import datetime
import pandas as pd

from structs.enumtype import XAxisRange


class WebInfoRakuten:
    url_login = 'https://www.rakuten-sec.co.jp/ITS/V_ACT_Login.html'
    id = {
        'auto-logout': 'changeAutoLogout',  # 自動ログアウトの状態
        'credit': 'linkBuyNew',  # 信用新規
        'domestic': 'gmenu_domestic_stock',  # 国内株式
        'domestic-stock-input-box': 'dscrCdNm2',  # 国内株式検索ボックス
        'update-status': 'autoUpdatePanelOffSelect',  # 株価更新ステータス
        'login': 'form-login-id',  # ログイン・アカウント
        'login-button': 'login-btn',  # ログイン・ボタン
        'passwd': 'form-login-pass',  # ログイン・パスワード
        'auto-update-off-select': 'autoUpdatePanelOffSelect',  # 自動手動選択
        'auto-update-on-select': 'autoUpdatePanelOnSelect',  # 自動停止選択
        'auto-update-off-status': 'autoUpdatePanelOffStatus',  # 自動更新OFF状態（パネル）
        'auto-update-on-status': 'autoUpdatePanelOnStatus',  # 自動更新ON状態（パネル）
        'auto-update-off-button': 'autoUpdateButtonOff',  # 自動更新 OFF ボタン
        'auto-update-on-button': 'autoUpdateButtonOn',  # 自動更新 ON ボタン
        'buy': 'buy',  # 買建
        'sell': 'sell',  # 売建
        'general_1d': 'general_1d',  # 一般（1日）
        'shares': 'orderValue',  # 数量 株/口（入力欄）
        'order-price': 'marketOrderPrice',  # 指値（入力欄）
        'market-order': 'priceMarket',  # 価格 成行で執行（ラジオボタン）
    }
    classname = {
        'auto-logout-button': 'pcm-gl-auto-logout-btn',  # 自動ログアウト ON/OFF
        'logout-button': 'pcm-gl-s-header-logout__btn',  # ログアウトボタン
        'domestic-stock-search-box': 'stock-search-box',  # 銘柄検索ボックス
        'domestic-stock-btn-box': 'btn-box',  # 銘柄検索ボタン
        'table-stock-price': 'tbl-stock-price',  # 株価テーブル
        'table-stock-price-value': 'price-01',  # 株価テーブル内の株価
        'table-stock-price-time': 'time-01',  # 株価テーブル内の時刻
    }
    title = {
        'home': 'ホーム | 楽天証券[PC]',
        'login': '総合口座ログイン | 楽天証券',
    }
    ticker = {
        '東京エレクトロン': '8035',
        'ＮＦ日経レバ': '1570',
        'ＳＣＲＥＥＮホールディングス': '7735',
        '三菱ＵＦＪフィナンシャルＧ': '8306'
    }

    dir_result = 'results'  # 取得した株価情報 (pickle) の保存先

    dt_now = datetime.datetime.now()
    ymd = str(dt_now.date())
    dt_start = pd.to_datetime('%s 09:00:00' % ymd)
    dt_end = pd.to_datetime('%s 15:30:00' % ymd)
    dt_noon1 = pd.to_datetime('%s 11:30:00' % ymd)
    dt_noon2 = pd.to_datetime('%s 12:30:00' % ymd)
    dt_ca = pd.to_datetime('%s 15:25:00' % ymd)

    xaxis_range = XAxisRange.DAY

    # y軸のスケール固定化
    yaxis_scale_fixed = False

    # 評価用指標の表示
    eval_index = False
    threshold_mtm = 15

    # 信用取引株の数量
    num_shares = '100'

    def __init__(self):
        self.ticker_target = ''

    def getPickleDir(self) -> str:
        return self.dir_result

    def getTickerTarget(self) -> str:
        return self.ticker_target

    def getXAxisRange(self) -> XAxisRange:
        return self.xaxis_range

    def setTargetTicker(self, ticker_target: str):
        self.ticker_target = ticker_target

    def setYMD(self, dt):
        ymd = str(dt.date())
        self.dt_start = pd.to_datetime('%s 09:00:00' % ymd)
        self.dt_end = pd.to_datetime('%s 15:30:00' % ymd)
        self.dt_noon1 = pd.to_datetime('%s 11:31:00' % ymd)
        self.dt_noon2 = pd.to_datetime('%s 12:30:00' % ymd)
        self.dt_ca = pd.to_datetime('%s 15:25:00' % ymd)

    def setXAxisRange(self, xaxis_range: XAxisRange):
        self.xaxis_range = xaxis_range
