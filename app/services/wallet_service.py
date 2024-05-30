from app.database.model.transaction import TransactionModel
from app.database.model.wallet import WalletModel

class WalletService():

    @staticmethod
    async def save_transaction():
        pass

    @staticmethod
    async def refresh_wallet(db_session):
        ticket_avg_list = await TransactionModel.calculate_avg(db_session)
        for ticket in ticket_avg_list:
            wallet = WalletModel()
            wallet.code = f'{ticket[0]}.SA'
            wallet.average_price = ticket[1] 
            wallet.number_of_shares = ticket[2]
            wallet.category = "STOCK"
            await WalletModel.save(wallet, db_session)
  