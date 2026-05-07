from unittest.mock import patch

from django.test import TestCase


class HealthViewTests(TestCase):
    def test_health_is_ok_when_database_is_ready(self):
        response = self.client.get('/health/', HTTP_HOST='localhost')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'ok')

    @patch('skillsphere.views.MigrationExecutor')
    def test_health_returns_503_when_migrations_are_pending(self, migration_executor_cls):
        executor = migration_executor_cls.return_value
        executor.loader.graph.leaf_nodes.return_value = [('skills', '0007_candidateskillprogress')]
        executor.migration_plan.return_value = [object()]

        response = self.client.get('/health/', HTTP_HOST='localhost')

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.content, b'pending migrations')
