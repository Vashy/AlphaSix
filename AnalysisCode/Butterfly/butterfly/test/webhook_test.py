import unittest
from Butterfly.butterfly.webhook import GLIssueWebhook, Path


class TestWebhook(unittest.TestCase):

    def test_gitlab_issue_webhook(self):
        whook = GLIssueWebhook()
        self.assertIsNone(whook.webhook())
        path = Path(__file__).parent.parent / 'webhook.json'

        whook.json_file = path
        whook.parse()
        wh = whook.webhook()

        self.assertEqual(wh["object_kind"], "issue")
        self.assertEqual(wh["project"]["id"], 1)
        self.assertEqual(wh["project"]["name"], "Gitlab Test")
        self.assertEqual(wh["action"], "open")
        self.assertEqual(wh["description"], "Create new API "
                         "for manipulations with repository")

        self.assertEqual(wh["assignees"][0], "user1")

        self.assertEqual(wh["labels"][0], "API")

        # TODO: Manca wh["changes"]

        self.assertRaises(FileNotFoundError, setattr, whook, 
                          "json_file", "fileeeeee")
        self.assertRaises(FileNotFoundError, setattr, whook,"json_file",
                          Path(__file__).parent / "fileeeeee")

        self.assertRaises(TypeError, setattr, whook, "json_file", 1)

        whook.json_file = None
        self.assertRaises(FileNotFoundError, whook.parse)


if __name__ == '__main__':
    unittest.main()
