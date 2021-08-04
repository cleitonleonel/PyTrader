# -*- coding: utf-8 -*-
#
import os
import io
import sys
import time
import json
import logging
import requests
import webbrowser
import PySimpleGUIQt as sg
from threading import Thread
from PIL import Image, ImageSequence
from random import randint
from datetime import datetime, date, timedelta
from iqoptionapi.stable_api import IQ_Option

try:
    from round_image import round_apply
except:
    pass

logging.disable(logging.DEBUG)

__version__ = 'beta-001'


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


try:
    f = open('file.txt', 'r')
except:
    with open('file.txt', 'w') as f:
        f.write(',,,')
        f.close()
    for line in open('file.txt', 'r').readlines():
        try:
            params = line.split(',')
            user_email = params[0]
            user_password = params[1]
            user_remember = params[2].replace('\n', '')
        except:
            pass


def get_currency():
    timer = datetime.now()
    dias = ('seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom')
    hj = date.today()
    dia = dias[hj.weekday()]
    if dia == 'sex' and timer.hour > 15 or dia == 'sab' or dia == 'dom' and timer.hour < 21:
        currency_list = [
            'USDJPY-OTC', 'USDCHF-OTC', 'NZDUSD-OTC', 'GBPUSD-OTC', 'EURUSD-OTC', 'EURJPY-OTC', 'EURGBP-OTC',
            'AUDCAD-OTC'
        ]
    else:
        currency_list = [
            'EURUSD', 'EURGBP', 'GBPJPY', 'EURJPY', 'GBPUSD', 'USDJPY', 'AUDCAD', 'NZDUSD', 'USDRUB', 'AMAZON', 'APPLE',
            'BAIDU',
            'CISCO', 'FACEBOOK', 'GOOGLE', 'INTEL', 'MSFT', 'YAHOO', 'AIG', 'CITI', 'COKE', 'GE', 'GM', 'GS', 'JPM',
            'MCDON', 'MORSTAN',
            'NIKE', 'USDCHF', 'XAUUSD', 'XAGUSD', 'ALIBABA', 'YANDEX', 'AUDUSD', 'USDCAD', 'AUDJPY', 'GBPCAD', 'GBPCHF',
            'GBPAUD', 'EURCAD',
            'CHFJPY', 'CADCHF', 'EURAUD', 'TWITTER', 'FERRARI', 'TESLA', 'USDNOK', 'EURNZD', 'USDSEK', 'USDTRY',
            'MMM:US', 'ABT:US', 'ABBV:US',
            'ACN:US', 'ATVI:US', 'ADBE:US', 'AAP:US', 'AA:US', 'AGN:US', 'MO:US', 'AMGN:US', 'T:US', 'ADSK:US',
            'BAC:US', 'BBY:US', 'BA:US',
            'BMY:US', 'CAT:US', 'CTL:US', 'CVX:US', 'CTAS:US', 'CTXS:US', 'CL:US', 'CMCSA:US', 'CXO:US', 'COP:US',
            'ED:US', 'COST:US',
            'CVS:US', 'DHI:US', 'DHR:US', 'DRI:US', 'DVA:US', 'DAL:US', 'DVN:US', 'DO:US', 'DLR:US', 'DFS:US',
            'DISCA:US', 'DOV:US', 'DTE:US',
            'DNB:US', 'ETFC:US', 'EMN:US', 'EBAY:US', 'ECL:US', 'EIX:US', 'EMR:US', 'ETR:US', 'EQT:US', 'EFX:US',
            'EQR:US', 'ESS:US', 'EXPD:US',
            'EXR:US', 'XOM:US', 'FFIV:US', 'FAST:US', 'FRT:US', 'FDX:US', 'FIS:US', 'FITB:US', 'FSLR:US', 'FE:US',
            'FISV:US', 'FLS:US', 'FMC:US',
            'FBHS:US', 'FCX:US', 'FTR:US', 'GILD:US', 'HAS:US', 'HON:US', 'IBM:US', 'KHC:US', 'LMT:US', 'MA:US',
            'MDT:US', 'MU:US', 'NFLX:US',
            'NEE:US', 'NVDA:US', 'PYPL:US', 'PFE:US', 'PM:US', 'PG:US', 'QCOM:US', 'DGX:US', 'RTN:US', 'CRM:US',
            'SLB:US', 'SBUX:US', 'SYK:US',
            'DIS:US', 'TWX:US', 'VZ:US', 'V:US', 'WMT:US', 'WBA:US', 'WFC:US', 'SNAP', 'DUBAI', 'TA25', 'AMD', 'ALGN',
            'ANSS', 'DRE', 'IDXX',
            'RMD', 'SU', 'TFX', 'TMUS', 'QQQ', 'SPY', 'BTCUSD', 'XRPUSD', 'ETHUSD', 'LTCUSD', 'DSHUSD', 'BCHUSD',
            'OMGUSD', 'ZECUSD', 'ETCUSD',
            'BTCUSD-L', 'ETHUSD-L', 'LTCUSD-L', 'BCHUSD-L', 'BTGUSD', 'QTMUSD', 'XLMUSD', 'TRXUSD', 'EOSUSD', 'USDINR',
            'USDPLN', 'USDBRL', 'USDZAR',
            'DBX', 'SPOT', 'USDSGD', 'USDHKD', 'LLOYL-CHIX', 'VODL-CHIX', 'BARCL-CHIX', 'TSCOL-CHIX', 'BPL-CHIX',
            'HSBAL-CHIX', 'RBSL-CHIX',
            'BLTL-CHIX', 'MRWL-CHIX', 'STANL-CHIX', 'RRL-CHIX', 'MKSL-CHIX', 'BATSL-CHIX', 'ULVRL-CHIX', 'EZJL-CHIX',
            'ADSD-CHIX', 'ALVD-CHIX',
            'BAYND-CHIX', 'BMWD-CHIX', 'CBKD-CHIX', 'COND-CHIX', 'DAID-CHIX', 'DBKD-CHIX', 'DPWD-CHIX', 'DTED-CHIX',
            'EOAND-CHIX', 'MRKD-CHIX',
            'SIED-CHIX', 'TKAD-CHIX', 'VOW3D-CHIX', 'PIRCM-CHIX', 'PSTM-CHIX', 'TITM-CHIX', 'CSGNZ-CHIX', 'NESNZ-CHIX',
            'ROGZ-CHIX', 'UBSGZ-CHIX',
            'SANE-CHIX', 'BBVAE-CHIX', 'TEFE-CHIX', 'AIRP-CHIX', 'HEIOA-CHIX', 'ORP-CHIX', 'AUDCHF', 'AUDNZD', 'CADJPY',
            'EURCHF', 'GBPNZD', 'NZDCAD',
            'NZDJPY', 'EURNOK', 'CHFSGD', 'EURSGD', 'USDMXN', 'JUVEM', 'ASRM', 'MANU', 'UKOUSD', 'XPTUSD', 'USOUSD',
            'W1', 'AUDDKK', 'AUDMXN', 'AUDNOK',
            'AUDSEK', 'AUDSGD', 'AUDTRY', 'CADMXN', 'CADNOK', 'CADPLN', 'CADTRY', 'CHFDKK', 'CHFNOK', 'CHFSEK',
            'CHFTRY', 'DKKPLN', 'DKKSGD', 'EURDKK',
            'EURMXN', 'EURTRY', 'EURZAR', 'GBPILS', 'GBPMXN', 'GBPNOK', 'GBPPLN', 'GBPSEK', 'GBPSGD', 'GBPTRY',
            'NOKDKK', 'NOKJPY', 'NOKSEK', 'NZDDKK', 'NZDMXN',
            'NZDNOK', 'NZDSEK', 'NZDSGD', 'NZDTRY', 'NZDZAR', 'PLNSEK', 'SEKDKK', 'SEKJPY', 'SGDJPY', 'USDDKK',
            'NZDCHF', 'GBPHUF', 'USDCZK', 'USDHUF',
            'CADSGD', 'EURCZK', 'EURHUF', 'USDTHB', 'IOTUSD-L', 'XLMUSD-L', 'NEOUSD-L', 'ADAUSD-L', 'XEMUSD-L',
            'XRPUSD-L', 'EEM', 'FXI', 'IWM', 'GDX',
            'XOP', 'XLK', 'XLE', 'XLU', 'IEMG', 'XLY', 'IYR', 'SQQQ', 'OIH', 'SMH', 'EWJ', 'XLB', 'DIA', 'TLT', 'SDS',
            'EWW', 'XME', 'QID', 'AUS200', 'FRANCE40',
            'GERMANY30', 'HONGKONG50', 'SPAIN35', 'US30', 'USNDAQ100', 'JAPAN225', 'USSPX500', 'UK100', 'TRXUSD-L',
            'EOSUSD-L', 'BNBUSD-L', 'ACB',
            'CGC', 'CRON', 'GWPH', 'MJ', 'TLRY', 'BUD', 'LYFT', 'PINS', 'ZM', 'UBER', 'MELI', 'BYND', 'BSVUSD-L',
            'ONTUSD-L', 'ATOMUSD-L', 'WORK', 'FDJP', 'CAN', 'VIAC', 'TFC'
        ]
    return currency_list


def check_image():
    image_path = resource_path("img-user.jpeg")
    if not os.path.isfile(image_path):
        number = randint(1, 5)
        user_image = resource_path(f'images/profile_{number}.png')
    else:
        user_image = image_path
    try:
        return round_apply(user_image)
    except:
        return user_image


def remember():
    for line in open('file.txt', 'r').readlines():
        if line.split(',')[2] == 'False':
            params = ['', '', False]
            return params
        try:
            params = line.split(',')
            user_email = params[0]
            user_password = params[1]
            user_remember = params[2].replace('\n', '')
            return params
        except:
            params = ['', '', False]
            return params


def checked(object):
    if not object or object == '' or object == 'False':
        return False
    return True


def get_img_data(filename, maxsize=(150, 100), format=None):
    if not format:
        format = 'PNG'
    img = Image.open(resource_path(filename))
    img.thumbnail(maxsize)
    bio = io.BytesIO()
    img.save(bio, format=format)
    del img
    return bio.getvalue()


def get_img_bytes(img_bytes, format=None):
    if not format:
        format = 'PNG'
    bio = io.BytesIO()
    img_bytes.save(bio, format=format)
    return bio.getvalue()


def download_image(url=None, file_path=None):
    image_path = resource_path('img-user.jpeg')
    if file_path:
        img = Image.open(file_path)
        img.save(image_path)
    elif not os.path.isfile(image_path):
        r = requests.get(url)
        im = Image.open(io.BytesIO(r.content))
        rgb_im = im.convert('RGB')
        rgb_im.save(image_path)


def open_browser(url):
    webbrowser.open_new(url)


def window_debuging(log):
    import PySimpleGUI as simplegui
    layout = [
        [simplegui.Text('')],
        [simplegui.Text(''), simplegui.Text(' ' * 10), simplegui.Text('Debug Log', font=("verdana", 18)),
         simplegui.Text(' ' * 2)],
        [simplegui.Text(' \n' * 2)],
        [simplegui.Text(''), simplegui.Text(' ' * 15), simplegui.Button('Close Window', pad=(1, 0)),
         simplegui.Text(' ' * 2)],
        [simplegui.Text('')],
        [simplegui.Multiline(default_text=log, size=(50, 30), key='Textbox')],
        [simplegui.Text(' \n' * 4)]
    ]
    window = simplegui.Window(f'RootTrader | Debuging', size=(300, 800)).Layout(layout)
    while True:
        button, values = window.Read()
        if button in (None, 'Close Window'):
            break
        print(values['Textbox'])
    window.close()


def get_img_frames(filename):
    gif_filename = resource_path(filename)
    sequence_frames = [get_img_bytes(img) for img in ImageSequence.Iterator(Image.open(gif_filename))]
    frame_duration = Image.open(gif_filename).info['duration']
    return sequence_frames, frame_duration


def animation_image(window):
    sequence, duration = get_img_frames('images/trading.gif')
    idx = 0
    while idx in range(1):
        for frame in sequence:
            window.read(timeout=duration)
            window['loading'].update(data=frame)
        idx += 1


def welcome_layout():
    layout1 = [
        [sg.Text('  \n' * 6)],
        [sg.Text(' ' * 2), sg.Image(data=get_img_data(filename="images/img-02.png")), sg.Text(' ' * 2)],
        [sg.Text('  \n' * 4)],
        [sg.Button('Login', button_color=('black', 'Green'), border_width=True, key='Login', size=(30, 1.1))],
        [sg.Text('  \n' * 3)],
        [sg.Text(' ' * 2), sg.Text('Ainda não é cliente?'), sg.Text(' ' * 2)],
        [sg.Text(' ' * 2), sg.Text('Acesse'), sg.Text('https://iqoption.com/pt', text_color='blue', enable_events=True,
                                                      font=('Courier New', 8, 'underline'), click_submits=True,
                                                      key='link'), sg.Text('e registre-se.'), sg.Text(' ' * 2)],
        [sg.Text(' \n' * 10)],
        [sg.Text(' ' * 10), sg.Text('Versão atual ' + __version__)]
    ]
    return layout1


def login_layout():
    layout2 = [
        [sg.Text(' \n' * 4)],
        [sg.Text(' ' * 2), sg.Image(data=get_img_data(filename="images/img-02.png"), size=(15, 15)),
         sg.Text(' ' * 2)],
        [sg.Text(' \n' * 4)],
        [sg.Text('E-mail: ')], [sg.Input(remember()[0], font=("Verdana", 13), key='email', focus=True, size=(30, 1.1))],
        [sg.Text('Senha: ')],
        [sg.Input(remember()[1], font=("Verdana", 13), key='senha', password_char='*', size=(30, 1.1))],
        [sg.Text('Remember-me')], [sg.Checkbox('', default=checked(remember()[2]), key='remember')],
        # [sg.Text(''), sg.Text('LOADING...', font=("verdana", 20), visible=False, key='loading'), sg.Text('')],
        [sg.Text(''), sg.Image(key='loading'), sg.Text('')],
        [sg.Text(' \n' * 5)],
        [sg.Button('Entrar', border_width=True, size=(30, 1.1), key='Entrar')]
    ]
    return layout2


def leader_layout(data):
    layout3 = [
        [sg.Text('')],
        [sg.Text(' ' * 2), sg.Text('TRADER SOFTWARE', font=("verdana", 18), text_color=True), sg.Text(' ' * 2)],
        [sg.Text(' ' * 3), sg.Text('Trader Expert', font=("verdana", 13), text_color=8), sg.Text(' ' * 5)],
        [sg.Text(' ' * 2), sg.Image(data=get_img_data(filename=check_image()), size_px=[0, 1], size=(15, 15)),
         sg.Text(' ' * 2)],
        # [sg.FileBrowse('Alterar', size=(7, 0.8), file_types=(("Imagens", "*jpg"), ("Imagens", "*jpeg"),
        # ("Imagens", "*png"),), key='Change', enable_events=True)],
        [sg.Button('Histórico', focus="True", border_width=True, size=(7, 0.8), pad=[0, 0], key='Debug',
                   enable_events=True, disabled=True), sg.Text(' ' * 2),
         sg.Button('Resultado', focus="True", border_width=True, size=(7, 0.8), pad=[0, 0], key='Status',
                   enable_events=True, disabled=True)],
        [sg.Text('Nome:', size=(4, 1)), sg.Text(data['name'], size=(10, 1)), sg.Text(' ' * 2),
         sg.Text('Saldo:', size=(4, 1)), sg.Text(data['balance_test'], key='saldo', size=(6, 1))],
        [sg.Txt('_' * 42)],
        [sg.Spin([i for i in range(0, 3)], initial_value=0, font=("verdana", 13), key="mhi", pad=[1, 0], size=(4, 1),
                 enable_events=True), sg.Txt('Mhi' * 1),
         sg.Radio('Seguro', 1, key='protect_profit', default=True, enable_events=True, size=(10, 1)),
         sg.Radio('Arriscado', 1, key='risky_operation', enable_events=True, size=(10, 1))],
        [sg.Txt('_' * 42)],
        [sg.Text('Stop Gain: '), sg.Text('Stop Loss: '), sg.Text('Martingale: '), sg.Text('Soros: ')],
        [sg.Input(0, font=("verdana", 13), key="gain", pad=[1, 0], size=(7.3, 1), enable_events=True),
         sg.Input(0, font=("verdana", 13), key="loss", pad=[1, 0], size=(7.3, 1), enable_events=True),
         sg.Input(0, font=("verdana", 13), key="gale", pad=[1, 0], size=(7.3, 1), enable_events=True),
         sg.Input(0, font=("verdana", 13), key="soros", pad=[1, 0], size=(7.3, 1), enable_events=True)
         ],
        [sg.Txt('_' * 42)],
        [sg.Text('Conta: '), sg.Text('Tipo de Conta: ')],
        [sg.Combo(['PRACTICE', 'REAL'], key="account", enable_events=True, size=(15, 1), readonly=True),
         sg.Combo(['DIGITAL', 'BINÁRIO'], key="account_type", size=(15, 1), readonly=True)],
        [sg.Text('Moeda: '), sg.Text('Valor:')],
        [sg.Combo(get_currency(), key="currency", size=(15, 1), visible_items=10),
         sg.Input('', font=("verdana", 13), key="value", pad=[1, 0], focus=True, size=(15, 1), enable_events=True)],
        [sg.Text('Duração: '), sg.Text('Tempo Restante: ')],
        [sg.Input('', font=("verdana", 13), key="duration", pad=[1, 0], size=(15, 1), enable_events=True),
         sg.Input('', text_color="black", justification='center', key="clock", font=("verdana", 13), pad=[1, 0], size=(15, 1))],
        [sg.Txt('_' * 42)],
        [sg.Txt('')],
        [sg.Button('Cima', button_color=('black', 'Green'), focus="True", border_width=True, pad=[1, 0], size=(7, 2)),
         sg.Text(' ' * 2),
         sg.Button('Baixo', button_color=('black', 'Red'), focus="True", border_width=True, pad=[1, 0], size=(7, 2)),
         sg.Text(' ' * 2),
         sg.Button('Stop', button_color=('black', 'Orange'), focus="True", border_width=True, pad=[1, 0], size=(7, 2))],
        [sg.Text(' \n' * 2)]
    ]
    return layout3


class RootThread(Thread):

    def __init__(self, func, **kwargs):
        super(RootThread, self).__init__()
        self.func = func
        self.args = kwargs
        self.result = None

    def run(self):
        time.sleep(2)
        self.result = self.func(**self.args)

    def get_result(self):
        Thread.join(self)
        try:
            return self.result
        except Exception:
            return None


class IQ_Trader(object):

    def __init__(self, e_mail, pass_word):
        self.email = e_mail
        self.password = pass_word
        self.time_trader = self.get_timer()
        self.profit = 0
        self.current_profit = None
        self.current_value = 0
        self.payout = None
        self.security_mode = None
        self.risky_mode = None
        self.stop_gain = None
        self.stop_loss = None
        self.gale = None
        self.mhi = None
        self.par = None
        self.enter = None
        self.first_enter = None
        self.direction = None
        self.time_frame = None
        self.account_type = None
        self.status = None
        self.id = None
        self.type = None
        self.remaning_time = None
        self.data = None
        self.sell_all = []
        self.log = []
        self.api = IQ_Option(self.email, self.password)

    def set_config(self, par, enter, direction, time_frame, type, balance='PRACTICE'):
        self.type = type
        self.account_type = balance
        self.par = par
        self.enter = int(enter)
        self.first_enter = self.enter
        self.time_frame = int(time_frame)
        self.direction = direction
        self.api.change_balance(balance)
        self.payout = self.get_payout()

        log = f'\n<<<CONFIGURAÇÕES DO TRADER>>>\n' \
              f'HORA DA ENTRADA: {self.get_timer()}\n' \
              f'TIPO  DE CONTA: {self.account_type}\n' \
              f'TIPO DE OPERAÇÃO: {self.type}\n' \
              f'ATIVOS: {self.par}\n' \
              f'VALOR DA ENTRADA: {str(self.enter)} R$\n' \
              f'DIREÇÃO: {self.direction}\n' \
              f'TEMPO DE OPERAÇÃO: {str(self.time_frame)} MINUTO(S)\n' \
              f'{"OPERANDO COM: " + str(self.gale) + " GALE(S) " if self.gale > 0 else ""}' \
              f'{chr(10) + "STOP-GAIN DE: " + str(self.stop_gain) if self.stop_gain > 0 else ""}' \
              f'{chr(10) + "E STOP-LOSS DE: " + str(self.stop_loss) if self.stop_loss > 0 else ""}'

        self.log.append(log)
        print(log)

    def get_config(self):
        return self.log

    def connect(self):
        return self.api.connect()

    def get_timer(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M')

    def get_buys(self):
        return self.sell_all

    def get_profile(self):
        return json.loads(json.dumps(self.api.get_profile_ansyc()))

    def get_user_profile(self, user_id):
        return self.api.get_user_profile_client(user_id)

    def stop(self):
        result = False
        if self.profit <= float('-' + str(abs(self.stop_loss))):
            print('Stop Loss batido!')
            self.data['stop_loss'] = True
            result = True
        if self.profit >= float(abs(self.stop_gain)):
            print('Stop Gain Batido!')
            self.data['stop_gain'] = True
            result = True
        return result

    def martingale(self):
        expected_profit = self.enter * self.payout
        loss = float(self.enter)
        while True:
            if round(self.enter * self.payout, 2) > round(abs(loss) + expected_profit, 2):
                return round(self.enter, 2)
            self.enter += 0.01

    def get_payout(self):
        self.api.subscribe_strike_list(self.par, 1)
        while True:
            self.current_profit = self.api.get_digital_current_profit(self.par, 1)
            if self.current_profit:
                self.current_profit = round(int(self.current_profit) / 100, 2)
                break
            time.sleep(1)
        self.api.unsubscribe_strike_list(self.par, 1)
        return self.current_profit

    def direction_by_candles(self):
        before_min = datetime.now() - timedelta(minutes=1)
        candles = self.api.get_candles(self.par, 60, 10, datetime.timestamp(before_min))

        candles[0] = 'g' if candles[0]['open'] < candles[0]['close'] else 'r' \
            if candles[0]['open'] > candles[0]['close'] else 'd'
        candles[1] = 'g' if candles[1]['open'] < candles[1]['close'] else 'r' \
            if candles[1]['open'] > candles[1]['close'] else 'd'
        candles[2] = 'g' if candles[2]['open'] < candles[2]['close'] else 'r' \
            if candles[2]['open'] > candles[2]['close'] else 'd'

        colors = candles[0] + ' ' + candles[1] + ' ' + candles[2]

        if colors.count('g') > colors.count('r') and colors.count('d') == 0:
            self.direction = ('put' if self.mhi == 1 else 'call')
        if colors.count('r') > colors.count('g') and colors.count('d') == 0:
            self.direction = ('call' if self.mhi == 1 else 'put')
        return self.direction

    def start(self):
        if not self.id:
            for idx in range(self.gale):
                self.status, self.id = self.api.buy_digital_spot(self.par, self.enter, self.direction, self.time_frame) \
                    if self.type == 'DIGITAL' else self.api.buy(self.enter, self.par, self.direction, self.time_frame)
                self.sell_all.append(self.id)
                result = self.awaiting_result(idx)
                if result:
                    return self.profit
                self.log.append(f'\nPRÓXIMA ENTRADA: {self.enter}\n')
                print(f'PRÓXIMA ENTRADA: {self.enter}')
            return self.start()
        else:
            return self.start_live()

    def start_live(self):
        for idx in range(self.gale):
            self.status, self.id = self.api.buy_digital_spot(self.par, self.enter, self.direction, self.time_frame) \
                if self.type == 'DIGITAL' else self.api.buy(self.enter, self.par, self.direction, self.time_frame)
            self.sell_all.append(self.id)
            result = self.awaiting_result(idx)
            if result:
                return self.profit
            self.log.append(f'\nPRÓXIMA ENTRADA: {self.enter}\n')
            print(f'PRÓXIMA ENTRADA: {self.enter}')
            if idx > 1 and self.security_mode:
                if self.profit < self.first_enter:
                    print('MODO SEGURO ATIVADO, LUCROS NEGATIVOS ABAIXO DE SUA PRIMEIRA ENTRADA, ABORTANDO...')
                elif self.enter > self.stop_loss:
                    print('ENTRADA MAIOR QUE O LIMITE DE PERDAS, ABORTANDO...')
                return self.profit
        return self.start()

    def awaiting_result(self, idx):
        if isinstance(self.id, int):
            print('\nAguarde a operação terminar!!!\n')
            self.api.subscribe_strike_list(self.par, self.time_frame)
            self.remaning_time = self.api.get_remaning(self.time_frame) - 30
            count = self.remaning_time + 30
            while True:
                self.data['profit_after_sale'] = f'{self.api.get_digital_spot_profit_after_sale(self.id):.2f} R$'
                monitor = f'\rLUCRO/PREJUÍZO ATUAL: {self.api.get_digital_spot_profit_after_sale(self.id):.2f} R$'
                print("", end=monitor)
                status, self.current_value = self.api.check_win_digital_v2(self.id) if self.type == 'DIGITAL' \
                    else self.api.check_win_v3(self.id)
                if status:
                    self.current_value = self.current_value if self.current_value > 0 \
                        else float('-' + str(abs(self.enter)))
                    self.profit += round(self.current_value, 2)
                    print('\nRESULTADO DA OPERAÇÃO: ', end='')
                    print('WIN /' if self.current_value > 0 else 'LOSS /', round(self.current_value, 2),
                          '/', round(self.profit, 2), ('/ ' + str(idx) + ' GALE' if idx > 0 else ''))
                    print(f'STOP-LOSS: {str(abs(self.stop_loss))}', f'LUCRO: {round(self.profit, 2)}',
                          f'STOP-WIN: {float(abs(self.stop_gain))}')
                    if self.mhi:
                        new_direction = self.direction_by_candles()
                        self.direction = new_direction
                        print(f'APLICANDO MHI, DIREÇÃO: {self.direction}')
                    if self.current_value > 0:
                        self.log.append(monitor)
                        self.log.append('\nRESULTADO DA OPERAÇÃO: WIN\n')
                        self.enter = self.first_enter
                        self.data['win'] = True
                        return self.stop()
                    else:
                        self.data['loss'] = True
                    self.log.append('RESULTADO DA OPERAÇÃO: LOSS')
                    self.enter = self.martingale()
                    return self.stop()
                time.sleep(1)
                count -= 1
                self.data['time'] = count


def long_operation_thread(fun):
    global rt_result
    fun.data = rt_result
    fun.start()


def create_window(layout, title):
    return sg.Window(f'RootTrader | {title}', size=[300, 800]).Layout(layout)


if __name__ == '__main__':
    layout = welcome_layout()
    window = create_window(layout, title='Welcome')
    profile = {}
    profile_dict = {}
    rt_result = {}
    timer_running, cont = '', 1
    iq_trader_id = None
    iq_trader = None
    task_rt = None
    only_numbers = True
    while True:
        button, values = window.Read(timeout=1.5)
        if button == sg.WIN_CLOSED:
            sys.exit(0)
        if button is None:
            break
        if button == 'loss' and len(values['loss']) > 5 or button == 'loss' \
                and values['loss'] and values['loss'][-1] not in '0123456789.':
            window['loss'].update(values['loss'][:-1])
            only_numbers = False
        if button == 'gain' and len(values['gain']) > 5 or button == 'gain' \
                and values['gain'] and values['gain'][-1] not in '0123456789.':
            window['gain'].update(values['gain'][:-1])
            only_numbers = False
        if button == 'gale' and len(values['gale']) > 1 or button == 'gale' \
                and values['gale'] and values['gale'][-1] not in '0123456789.':
            window['gale'].update(values['gale'][:-1])
            only_numbers = False
        if button == 'value' and len(values['value']) > 5 or button == 'value' \
                and values['value'] and values['value'][-1] not in '0123456789.':
            window['value'].update(values['value'][:-1])
        if button == 'duration' and len(values['duration']) > 2 or button == 'duration' \
                and values['duration'] and values['duration'][-1] not in '0123456789.':
            window['duration'].update(values['duration'][:-1])
        if button == 'link':
            open_browser("https://iqoption.com/pt/register")
        if button == 'Change':
            download_image(file_path=values['Change'][0])
        if button == 'Login':
            window.close()
            layout = login_layout()
            window = create_window(layout, title='Login')
        if button == 'Entrar':
            rt_email = values['email']
            rt_senha = values['senha']
            if values['remember']:
                remember()
                if rt_email != '' and rt_senha != '':
                    with open('file.txt', 'w') as file:
                        file.write(rt_email + ',' + rt_senha + ',' + str(values['remember']) + ',\n')
                        file.close()
            else:
                with open('file.txt', 'w') as file:
                    file.write('' + ',' + '' + ',' + str(values['remember']) + ',\n')
                    file.close()
            rt_trader = True
            animation_image(window)
            if rt_trader:
                iq_email = rt_email
                iq_password = rt_senha
                iq_trader = IQ_Trader(iq_email, iq_password)
                animation_image(window)
            window['loading'].Update(visible=False)
            window['Entrar'].Update('LOGADO COM SUCESSO', button_color=('white', 'green'))
            window.Refresh()
            check, reason = iq_trader.connect()
            if check:
                profile = iq_trader.get_profile()
                user_id = profile['user_id']
                user_profile = iq_trader.get_user_profile(user_id)
                if user_profile.get("img_url"):
                    download_image(user_profile["img_url"])
                profile_dict["balance_real"] = f"{profile['balance']:,.2f}"
                profile_dict["balance_test"] = f"{iq_trader.api.get_balance():,.2f}"
                profile_dict["iq_email"] = profile["email"]
                profile_dict["img_url"] = user_profile.get("img_url")
                profile_dict["name"] = ' '.join(profile["name"].split(' ')[::2]).capitalize()
                profile_dict["nationality"] = profile["nationality"]
                profile_dict["currency"] = profile["currency"]
                profile_dict["city"] = profile["city"]
                profile_dict["address"] = profile["address"]
            window.close()
            layout = leader_layout(profile_dict)
            window = create_window(layout, title='Leader')
        try:
            if values['account']:
                if values['account'] == 'PRACTICE':
                    window['saldo'].Update(f"{iq_trader.api.get_balance():,.2f}")
                    window.Refresh()
                elif values['account'] == 'REAL':
                    window['saldo'].Update(f"{profile['balance']:,.2f}")
                    window.Refresh()
        except:
            pass
        if button == 'Debug':
            window_debuging(iq_trader.get_config())
        if button == 'Cima' or button == 'Baixo' or button == 'Stop':
            direction = None
            account_type = None
            if button != 'Stop':
                if button == 'Cima':
                    direction = 'call'
                if button == 'Baixo':
                    direction = 'put'
                if values['account_type'] == 'DIGITAL':
                    account_type = 'live-deal-digital-option'
                if values['account_type'] == 'BINÁRIO':
                    account_type = 'live-deal-binary-option-placed'
                if only_numbers:
                    # iq_trader.soros = int(values['soros'])  if values['soros'] > 0 else None
                    iq_trader.gale = int(values['gale']) if values['gale'] != '' else 0
                    iq_trader.mhi = int(values['mhi']) if values['mhi'] > 0 else None
                    iq_trader.stop_gain = float(values['gain']) if values['gain'] != '' else 0
                    iq_trader.stop_loss = float(values['loss']) if values['loss'] != '' else 0
                    iq_trader.gale += 1

                iq_trader.profit = 0
                iq_trader.risky_mode = values['risky_operation']
                iq_trader.security_mode = values['protect_profit']
                iq_trader.set_config(par=values['currency'], enter=int(values['value']), direction=direction,
                                     time_frame=int(values['duration']), type=values['account_type'],
                                     balance=values['account'])
                task_rt = Thread(target=long_operation_thread, args=(iq_trader, ), daemon=True)
                task_rt.start()
                iq_trader_id = iq_trader.id
                total_orders = iq_trader.sell_all
                window['Debug'].Update(disabled=False)
                window['Debug'].Update(button_color=('white', 'green'))
                window.Refresh()
            else:
                total_orders = iq_trader.sell_all
                if len(total_orders) > 0:
                    print('VENDENDO, SÃO ' + str(len(total_orders)) + ' ORDENS AGORA...')
                    print(iq_trader.api.sell_option(total_orders))
                    iq_trader.sell_all = []
        if rt_result.get('win'):
            rt_result.pop('win')
            window['Status'].Update('Win', button_color=('white', 'green'))
            window['saldo'].Update(f"{iq_trader.api.get_balance():,.2f}")
            window.Refresh()
        elif rt_result.get('loss'):
            rt_result.pop('loss')
            window['Status'].Update('Loss', button_color=('white', 'red'))
            window['saldo'].Update(f"{iq_trader.api.get_balance():,.2f}")
            window.Refresh()
        if rt_result.get('time') and rt_result.get('time') >= 0:
            window['clock'].Update(time.strftime("   %H : %M : %S   ", time.gmtime(int(rt_result.get("time")))),
                                   text_color="black", font=("verdana", 13))
        if rt_result.get('time') and rt_result.get('time') < 0:
            window['clock'].Update('Operação concluída!!!', text_color='red', font=("verdana", 10))
        time.sleep(0.1)
    window.close()
quit()
