import alpaca_trade_api as tradeapi

api = tradeapi.REST('keyid', 'secretkey')
account = api.get_account()
api.list_positions()
api.submit_order(
    symbol='SPY',
    side='buy',
    type='market',
    qty='100',
    time_in_force='day',
    order_class='bracket',
    take_profit=dict(
        limit_price='305.0',
    ),
    stop_loss=dict(
        stop_price='295.5',
        limit_price='295.5',
    )
)