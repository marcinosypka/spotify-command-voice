import spotipy.util as util

from SpotifyWithPlayer import SpotifyWithPlayer
from data.data_utils import normalize_sentence
from data.pattern import get_commands
from numerals.numerals_evaluator import NumeralsNormalizer, NumeralsTransformer

scope = 'user-modify-playback-state user-read-currently-playing user-read-playback-state'
username = '26yuotyu35tiipythyrrs7jox04v5'
client_id = '9c862d0167b04dcd9ae3de8fc25d509b'
client_secret = '6a7729412eb442b794b5ce623beca996'
redirect_uri = 'http://localhost.com'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = SpotifyWithPlayer(auth=token)


sentence = r'wróć do poprzedniego, daj następny, jedenaście stop, przesuń na , idź do jeden koma dwadzieścia, przejdź ' \
           r'do trzy kropka trzynaście , przewiń na dwa dwukropek sto dwadzieścia cztery, przewiń na dwa dwukropek ' \
           r'cztery, przejdź do cztery kropka zero'

normalized_sentence = normalize_sentence(sentence)
numerals_normalizer = NumeralsNormalizer('numerals/numerals.txt')
transformer = NumeralsTransformer(numerals_normalizer)
normalized_numerals_sentence = transformer.replace_with_numbers(normalized_sentence)

get_commands(normalized_numerals_sentence, 'data/updated_results_manual.txt', debug=True)
