from iebank_api.models import Account
from iebank_api import db
from iebank_api.models import BankTransfer

def test_bank_transfer_object_process(testing_client):
        with testing_client.application.app_context():
            # Create Origin Account
            from_account = Account(name='Adrian checkin Account', country='Spain', currency='€', balance=1000.0)
            db.session.add(from_account)
            db.session.commit()
            # Create Destination Account
            to_account = Account(name='Daniel checkin Account', country='Spain', currency='€', balance=0.0)
            db.session.add(to_account)
            db.session.commit()

            # Transfer 100€ from Adrian to Daniel
            transfer = BankTransfer(from_account, to_account, 100.0)
            transfer_result = transfer.process_transfer()
            assert transfer_result == True
            assert from_account.balance == 900.0
            assert to_account.balance == 100.0


    
