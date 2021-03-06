from django.db.models import F, Sum, QuerySet
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, TrigramSimilarity as trgm_sim)
from itertools import chain
from .models import Article, Folder

USER_MODEL = get_user_model()


def article_fulltext_search(queryset: QuerySet, query: str) -> QuerySet:
    """
    Takes a queryset from the Article model and performs a
    full text search over it on the title and content columns.

    Args:
        (queryset) required: A queryset from the Artcile model.
        (query) required: The search query.
    """

    vector_query = SearchQuery(query)
    article_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')

    queryset = (queryset
                .annotate(rank=SearchRank(article_vector, vector_query),
                          similarity=trgm_sim('title', query),
                          score=Sum(
                              F('rank') + F('similarity') + trgm_sim('content', query))
                          )
                .filter(score__gte=0.1)
                )

    return queryset


def folder_fulltext_search(queryset: QuerySet, query: str) -> QuerySet:
    """
    Takes a queryset from the Folder model and performs a
    full text search over it on the name column.

    Args:
        (queryset) required: A queryset from the Folder model.
        (query) required: The search query.
    """

    vector_query = SearchQuery(query)
    folder_vector = SearchVector('name', weight='A')

    queryset = (queryset
                .annotate(rank=SearchRank(folder_vector, vector_query),
                          similarity=trgm_sim('name', query),
                          score=Sum(F('rank') + (F('similarity'))))
                .filter(score__gte=0.1)
                )

    return queryset


def get_knowledgebase(folder_id: int, kb_user: USER_MODEL,
                      request_user: USER_MODEL) -> list:
    """
    Fetches the content of a folder from the provided id and kb_user.

    Args:
        (folder_id) required: The folder to get the content for.
        (kb_user) required: The user of the knowledgebase being fetched.
        (request_user) required: The request user.
    """

    folders = (Folder
               .objects
               .filter(owner=kb_user, parent_folder=folder_id)
               )
    articles = (Article
                .objects
                .filter(author=kb_user,
                        folder=folder_id,
                        version_status_id=Article.Version_Status.ACTIVE)
                )
    try:
        foreign_articles = (USER_MODEL
                            .objects
                            .get(id=kb_user.id)
                            .foreign_articles
                            .annotate(article_user_id=F('article_user__id'))
                            .filter(article_user__folder=folder_id)
                            .select_related('author')
                            )
    except USER_MODEL.DoesNotExist:
        foreign_articles = []

    if request_user != kb_user:
        articles = articles.filter(article_status_id=Article.Article_Status.PUBLISHED)

    folder_content = list(chain(folders, articles, foreign_articles))

    folder_content.sort(key=lambda x: x.name.lower()
                        if isinstance(x, Folder) else x.title.lower())

    return folder_content


def search_knowledgebase(query: str, kb_user: USER_MODEL,
                         request_user: USER_MODEL) -> list:
    """
    Searches a users knowledgbase and returns the most
    relevant results.

    Args:
        (query) required: The query to search the knowledgbase.
        (kb_user) required: The user of the knowledgebase being fetched.
        (request_user) required: The request user.
    """

    folders = Folder.objects.filter(owner=kb_user)
    folders = folder_fulltext_search(folders, query)

    articles = Article.objects.filter(author=kb_user,
                                      version_status_id=Article.Version_Status.ACTIVE)
    articles = article_fulltext_search(articles, query)

    try:
        foreign_articles = (USER_MODEL
                            .objects
                            .get(id=kb_user.id)
                            .foreign_articles
                            .annotate(article_user_id=F('article_user__id'))
                            .all()
                            )
        foreign_articles = article_fulltext_search(foreign_articles, query)
    except USER_MODEL.DoesNotExist:
        foreign_articles = []

    if request_user != kb_user:
        articles = articles.filter(article_status_id=Article.Article_Status.PUBLISHED)

    folder_content = list(chain(folders, articles, foreign_articles))

    folder_content.sort(key=lambda x: x.name.lower()
                        if isinstance(x, Folder) else x.title.lower())

    return folder_content
