

   This project is an idea inspired by the following blog: 
   can be found at https://medium.com/crypto-currently/lets-build-the-tiniest-blockchain-e70965a248b
   I have renamed the coin into mamba coin, b/c kobe rules
   but all credit still goes to the original author of the blogpost

	few things added: 
		1. a way to sync nodes, transactions
		2. all transactions are broadcasted
		3. added detail implementation of mining, include syncing before and after, calling /clear_trans api to others
		4. added feature to Block class with current_hash
		5. thats all I can think of right now...

	future improvements: 
		1. a more secure block consensus
		2. a more secure transaction consensus
		3. a more secure post transaction api (with transaction checking) 
		4. a tougher proof of work
		5. GUI interface, web user interface to see wallet amounts (have to be a separete class) 
		6. thats all I can think of right now...


	BEFORE PRODUCTION DEPLOYMENT: 
		1. Intergration Testing
		2. System Testing

