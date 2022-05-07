from django.db.models import F, Value, Sum, Q
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, TrigramSimilarity as trgm_sim)
from itertools import chain
from .models import Article, Folder

def search_knowledgebase(query: str, kb_user, request_user) -> list:
    user_model = get_user_model()
    vector_query = SearchQuery(query)
    folder_vector = SearchVector('name', weight='A')
    article_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')

    folders = (Folder
               .objects
               .annotate(rank=SearchRank(folder_vector, vector_query),
                         similarity=trgm_sim('name', query),
                         score=Sum(F('rank') + (F('similarity'))))
               .filter(owner=kb_user, score__gte=0.1)
               )
    articles = (Article
                .objects
                .annotate(rank=SearchRank(article_vector, vector_query),
                          similarity=trgm_sim('title', query),
                          score=Sum(
                              F('rank') + F('similarity') + trgm_sim('content', query))
                          )
                .filter(author=kb_user,
                        score__gte=0.1,
                        version_status_id=Article.Version_Status.ACTIVE)
                )

    try:
        foreign_articles = (user_model
                            .objects
                            .get(id=kb_user.id)
                            .foreign_articles
                            .annotate(rank=SearchRank(article_vector, vector_query),
                                      similarity=trgm_sim('title', query),
                                      article_user_id=F('article_user__id'),
                                      score=Sum(
                                          F('rank') + F('similarity') + trgm_sim('content', query))
                                      )
                            .filter(score__gte=0.1)
                            )
    except user_model.DoesNotExist:
        foreign_articles = []

    if request_user != kb_user:
        articles = articles.filter(article_status_id=Article.Article_Status.PUBLISHED)

    return list(chain(folders, articles, foreign_articles))


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
