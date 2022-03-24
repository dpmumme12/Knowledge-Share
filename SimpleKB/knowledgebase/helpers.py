from django.db.models import F, Value, Sum
from django.contrib.postgres.search import (SearchQuery, SearchVector,
                                            SearchRank, TrigramSimilarity as trgm_sim)
from .models import Article, Folder

def search_knowledgebase(query, user):
    vector_query = SearchQuery(query)
    folder_vector = SearchVector('name', weight='A')
    article_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')

    folders = (Folder
               .objects
               .annotate(object_type=Value('folder'),
                         rank=SearchRank(folder_vector, vector_query),
                         similarity=trgm_sim('name', query),
                         score=Sum(F('rank') + (F('similarity'))))
               .filter(owner=user, score__gte=0.1)
               .only('name')
               )
    articles = (Article
                .objects
                .annotate(name=F('title'), object_type=Value('article'),
                          rank=SearchRank(article_vector, vector_query),
                          similarity=trgm_sim('name', query),
                          score=Sum(F('rank') + F('similarity') + trgm_sim('content', query)))
                .filter(author=user, score__gte=0.1)
                .only('id')
                )

    return folders.union(articles).order_by('-score')
