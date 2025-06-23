from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, ChatSessionViewSet, ChunkViewSet, DocumentViewSet, EmbeddingViewSet

router = DefaultRouter()
router.register(r'chatmessages', ChatMessageViewSet)
router.register(r'chatsessions', ChatSessionViewSet)
router.register(r'chunks', ChunkViewSet)
router.register(r'documents', DocumentViewSet)
router.register(r'embeddings', EmbeddingViewSet)

urlpatterns = router.urls
