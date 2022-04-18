from django.db.models import F, Value, Sum, Q
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, TrigramSimilarity as trgm_sim)
from itertools import chain
from .models import Article, Folder

def search_knowledgebase(query: str, user: object):
    vector_query = SearchQuery(query)
    folder_vector = SearchVector('name', weight='A')
    article_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')

    folders = (Folder
               .objects
               .annotate(rank=SearchRank(folder_vector, vector_query),
                         similarity=trgm_sim('name', query),
                         score=Sum(F('rank') + (F('similarity'))))
               .filter(owner=user, score__gte=0.1)
               )
    articles = (Article
                .objects
                .annotate(rank=SearchRank(article_vector, vector_query),
                          similarity=trgm_sim('title', query),
                          score=Sum(F('rank') + F('similarity') + trgm_sim('content', query)))
                .filter(author=user, score__gte=0.1)
                )

    return list(chain(folders, articles))


def publish_article(article: Article):
    (Article
     .objects
     .filter(Q(uuid=article.uuid), ~Q(id=article.id))
     .update(article_status=Article.Article_Status.ARCHIVED,
             version_status=Article.Version_Status.HISTORY)
     )

    article.article_status = Article.Article_Status.PUBLISHED
    article.Version_Status = Article.Version_Status.ACTIVE
    article.save()

    return article


def create_new_version(article: Article):
    Article.objects.filter(uuid=article.uuid, version_status=Article.Version_Status.NEW_VERSION)
