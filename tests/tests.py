from io import StringIO

from django.core.management import call_command
from django.test import SimpleTestCase

from rungunicorn.management.commands.rungunicorn import Command


class ManageRungunicorn(SimpleTestCase):
    def setUp(self):
        def monkey_run(*args, **options):
            return

        self.output = StringIO()
        self.cmd = Command(stdout=self.output)
        self.cmd.gunicorn.run = monkey_run

    def assertServerSettings(self, bind):
        self.assertEqual(self.cmd.gunicorn.cfg.bind, bind)

    def test_runserver_bind(self):
        call_command(self.cmd)
        self.assertServerSettings(["127.0.0.1:8000"])

        call_command(self.cmd, bind=["1.2.3.4:8000", "1.2.3.4:8001"])
        self.assertServerSettings(["1.2.3.4:8000", "1.2.3.4:8001"])
