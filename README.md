# Banking-APPLICATION-gRPC

Problem Statement
The project's goal is to create a banking application based on gRPC that mimics interactions between clients and branches in a distributed system. Numerous financial procedures, including deposits, withdrawals, balance queries, and money transfers, must be handled by the system. The task is to efficiently build and execute this system while ensuring dependable and robust customer and branch communication.

Goal
Creating a distributed banking system that enables many clients to execute transactions (withdrawals or deposits) from different bank branches is the aim described in the issue statement. This approach assumes that each client has a unique branch assignment and a shared bank account. It also assumes that the account is not undergoing any concurrent modifications.
Each branch is in charge of keeping an accurate duplicate of the account balance that is synced with copies in other branches. Customers only communicate with the specified branch, which is identifiable by a specific ID.


Implementation Processes : - 
There are 3 files created : the files created are as follows : 1 Branch.py
2. Customer.py
3. project.proto

Steps :
1.At first I created proto file in which service called bank is defined specifying the request and response message formats for customer-branch interactions
2.in customer.py file –
• the Customer class is designed to represent individual customers. It maintains a list of events, interactions with branches, and communication channels.
• It supports actions like deposits, withdrawals, and balance inquiries.
• Customers are instantiated based on the data provided in a JSON file.
• The gRPC library is used to establish connections to branches, and the executeEvents method is responsible for sending events to the respective branch and receiving responses.
3. in branch.py file –
• The Branch class represents a branch in the distributed banking system.
• It communicates with other branches and customers using gRPC.
• The Branch class is responsible for handling customer requests, updating balances, and ensuring transactions are propagated among branches.
• Additionally, it handles money transfers between branches.

Results
The results are stored in the output.json file in the format described and final balance is 400
