# orders/utils.py
def notify_line_dummy(order, product, status):
    """
    LINE通知のダミー関数
    status: "success" or "cancel" を想定
    """
    message = f"[LINE通知ダミー] 注文ID={order.id} / 商品={product.name} / 状態={status}"
    print(message)  # 本物のLINE通知の代わりにターミナルへ出す
    return message