import random
from django.utils import timezone


def get_recommendations(user, all_events):
    from .models import Registration

    registered_ids = set(
        Registration.objects.filter(user=user).values_list('event_id', flat=True)
    )
    unregistered = [e for e in all_events if e.id not in registered_ids]

    if not registered_ids or not unregistered:
        upcoming = [e for e in unregistered if e.date >= timezone.now()]
        random.shuffle(upcoming)
        return upcoming[:3]

    registered = [e for e in all_events if e.id in registered_ids]
    user_tags = ' '.join(e.tags for e in registered if e.tags)

    if not user_tags.strip():
        upcoming = [e for e in unregistered if e.date >= timezone.now()]
        random.shuffle(upcoming)
        return upcoming[:3]

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        candidate_tags = [e.tags if e.tags else e.name for e in unregistered]
        corpus = [user_tags] + candidate_tags

        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]

        top_indices = similarities.argsort()[::-1][:3]
        return [unregistered[i] for i in top_indices]
    except Exception:
        upcoming = [e for e in unregistered if e.date >= timezone.now()]
        random.shuffle(upcoming)
        return upcoming[:3]
