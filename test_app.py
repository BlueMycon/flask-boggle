from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            # test that you're getting a template
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Homepage", html)

    def test_api_new_game(self):
        """Test starting a new game."""
        with self.client as client:
            # make a post request to /api/new-game
            resp = client.post("/api/new-game")
            # get the response body as json using .get_json()
            json_data = resp.get_json()
            # test that the game_id is a string
            game_id = json_data["gameId"]
            self.assertEqual(type(game_id), str)
            # test that the board is a list
            self.assertEqual(type(json_data["board"]), list)
            # board = json_data["board"]
            # for row in board:
            #     self.assertEqual(type(row), list)
            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIn(game_id, games)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:

            # make a post request to /api/new-game
            resp = client.post('/api/new-game')
            # get the response body as json using .get_json()
            data = resp.get_json()
            # find that game in the dictionary of games (imported from app.py above)
            game_id = data["gameId"]
            game = games[game_id]
            print(game.board)
            # manually change the game board's rows so they are not random
            game.board =  [['g','c','a','t','x'],
                          ['z','z','z','z','z'],
                          ['z','z','z','z','z'],
                          ['z','z','z','z','z'],
                          ['z','z','z','z','z']]
            # test to see that a valid word on the altered board returns {'result': 'ok'}
            resp_score_word = client.post('/api/score-word', json={"gameId": game_id, "word": "cat"})
            data = resp_score_word.get_json()
            print("data is=", data)
            self.assertEqual({'result': 'ok'}, data)
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            resp_score_word = client.post('/api/score-word', json={"gameId": game_id, "word": "henry"})
            data = resp_score_word.get_json()
            self.assertEqual({'result': 'not-on-board'}, data)
            # test to see that an invalid word returns {'result': 'not-word'}
            resp_score_word = client.post('/api/score-word', json={"gameId": game_id, "word": "henryyy"})
            data = resp_score_word.get_json()
            self.assertEqual({'result': 'not-word'}, data)