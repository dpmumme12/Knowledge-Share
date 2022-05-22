from django.db.models import F, Value, Sum, Q, QuerySet
from typing import Union, List
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, TrigramSimilarity as trgm_sim)
from itertools import chain
from .models import Article, Folder

USER_MODEL = get_user_model()

def search_knowledgebase(query: str, kb_user, request_user) -> list:
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


def get_knowledgebase(folder_id, kb_user, request_user):
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
                            .get(id=kb_user.id, article_user__folder=folder_id)
                            .foreign_articles
                            .annotate(article_user_id=F('article_user__id'))
                            .filter()
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


def publish_article(article: Article) -> Article:
    (Article
     .objects
     .filter(Q(uuid=article.uuid), ~Q(id=article.id))
     .update(article_status_id=Article.Article_Status.ARCHIVED,
             version_status_id=Article.Version_Status.HISTORY)
     )

    article.article_status_id = Article.Article_Status.PUBLISHED
    article.version_status_id = Article.Version_Status.ACTIVE
    article.save()

    return article


def create_new_version(article: Article) -> Article:
    (Article
     .objects
     .filter(uuid=article.uuid, version_status_id=Article.Version_Status.NEW_VERSION)
     .delete()
     )
    new_version = (Article
                   .objects
                   .create(author=article.author,
                           title=article.title,
                           slug=article.slug,
                           article_status_id=Article.Article_Status.DRAFT,
                           content=article.content,
                           version=article.version + 1,
                           version_status_id=Article.Version_Status.NEW_VERSION,
                           uuid=article.uuid,
                           folder=article.folder
                           )
                   )

    return new_version


def folder_fulltext_search(queryset: QuerySet, query: str) -> QuerySet:
    vector_query = SearchQuery(query)
    folder_vector = SearchVector('name', weight='A')

    queryset = (queryset
                .annotate(rank=SearchRank(folder_vector, vector_query),
                          similarity=trgm_sim('name', query),
                          score=Sum(F('rank') + (F('similarity'))))
                .filter(score__gte=0.1)
                )

    return queryset


def article_fulltext_search(queryset: QuerySet, query: str) -> QuerySet:
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
