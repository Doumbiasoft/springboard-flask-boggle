from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

boggle_board="board"
high_score="high_score"
number_of_play="number_of_play"
board_size="board_size"

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        

    def test_index(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/index')
            self.assertIn(boggle_board, session)
            self.assertIsNone(session.get(board_size))
            self.assertIsNone(session.get(high_score))
            self.assertIsNone(session.get(number_of_play))
            self.assertIn(b'<p><strong>High Score:</strong>', response.data)
            self.assertIn(b'<p><strong>Score:</strong>', response.data)
            self.assertIn(b'<p><strong>Seconds remain:</strong>', response.data)

    def test_start(self):
        """Make sure the board size selection HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn(b'<form action="/start-game" method="POST">', response.data)
            self.assertIn(b'<option value="4"> 4 x 4 </option>', response.data)
            self.assertIn(b'<option value="5"> 5 x 5 </option>', response.data)
            self.assertIn(b'<option value="6"> 6 x 6 </option>', response.data)
            self.assertIn(b'<option value="7"> 7 x 7 </option>', response.data)
            self.assertIn(b'<option value="8"> 8 x 8 </option>', response.data)
            self.assertIn(b'<option value="8"> 8 x 8 </option>', response.data)

    def test_start_default_board_size(self):
        """Make sure the default board size is in session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[boggle_board] = 4
            
        self.client.get('/index')
        self.assertEqual(sess[boggle_board], 4)
            

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess[boggle_board] = [["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"], 
                                 ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/index')
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/index')
        response = self.client.get(
            '/check-word?word=azertyuiopqsdfghjklmwxcvbn')
        self.assertEqual(response.json['result'], 'not-word')

