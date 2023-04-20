from io import BytesIO
from datetime import datetime
from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from openpyxl import load_workbook
from app.database.model.transaction import TransactionModel


class TransactionService():
    '''Transaction Service class'''

    @staticmethod
    async def import_transactions(file: UploadFile, db: AsyncSession ):
        """It read an excel file provided by B3 and import the data into database

        Args:
            file (UploadFile): Excel file provided by B3
            db (AsyncSession): database session
        """        
        buffer = BytesIO(file.file.read())
        wb = load_workbook(buffer, read_only=True)
        ws = wb.active

        rows = ws.iter_rows(values_only=True)
        file_header = next(rows) 
        rows = list(rows)
        for _, row in enumerate(rows):
            if row[file_header.index('Movimentação')] == 'Transferência - Liquidação':
                transaction = TransactionModel()
                transaction.effective_date = datetime.strptime(row[file_header.index('Data')], '%d/%m/%Y')
                transaction.broker = row[file_header.index('Instituição')]   
                transaction.code = row[file_header.index('Produto')].split('-')[0].strip()   
                transaction.action = 'BUY'
                transaction.num_shares = int(row[file_header.index('Quantidade')])   
                transaction.price = float(row[file_header.index('Preço unitário')])   
                transaction.total = float(row[file_header.index('Valor da Operação')])   
                await TransactionModel.save(transaction, db)
                