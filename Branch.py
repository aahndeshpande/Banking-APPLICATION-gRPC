import grpc
import project_pb2
import project_pb2_grpc
import json
from concurrent import futures
import sys


class Branch(project_pb2_grpc.BankServicer):

    def __init__(self, id, balance, branches):
        # unique ID of the Branch
        self.id = id
        # replica of the Branch's balance
        self.balance = balance
        # the list of process IDs of the branches
        self.branches = branches
        # the list of Client stubs to communicate with the branches
        self.stubList = list()
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # iterate the processID of the branches
        self.ChannelLIST=list()
       
        # TODO: students are expected to store the processID of the branches
        
        pass

class Branch(project_pb2_grpc.BankServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = self.initialize_stubs()

    def initialize_stubs(self):
        stubs = []
        for port in self.branches:
            if port != self.id:
                #channel to connect to other branches
                channel = grpc.insecure_channel(f'localhost:{50051 + port}')
                stub = project_pb2_grpc.BankStub(channel)
                stubs.append(stub)
        return stubs

    def MsgDelivery(self, request, context):
        interface = request.interface
        if interface == "query":
            return self.Query(request, context)
        elif interface == "deposit":
            return self.Deposit(request, context)
        elif interface == "withdraw":
            return self.Withdraw(request, context)
        elif interface == "propagate-withdraw":
            #balance propagation among branches for withdrawing money
            self.balance -= request.money
            self.propagating_balance(request.money,interface)
            return self.Query(request, context)
        elif interface == "propagate-deposit":
            #balance propagation among branches for deposit money
            self.balance += request.money
            self.propagating_balance(request.money,interface)
            return self.Query(request, context)
        elif interface == "transfer":
            return self.Transfer(request, context)

    def Query(self, request, context):
         #  for query request , returns the balance of current branch
        return project_pb2.MsgDeliveryReply(
            id=request.id, money=self.balance, result="success", interface=request.interface
        )

    def Deposit(self, request, context):
        self.balance += request.money
        self.propagating_balance(request.money)
        return project_pb2.MsgDeliveryReply(
            id=request.id, money=self.balance, result="success", interface=request.interface
        )

    def Withdraw(self, request, context):
        if self.balance >= request.money:
            self.balance -= request.money
            self.propagating_balance(-request.money)
            return project_pb2.MsgDeliveryReply(
                id=request.id, money=self.balance, result="success", interface=request.interface
            )
        else:
            return project_pb2.MsgDeliveryReply(
                id=request.id, money=self.balance, result="failure", interface=request.interface
            )

    def propagating_balance(self, amount,inter):
        for stub in self.stubList:
            stub.MsgDelivery(
                project_pb2.MsgDeliveryRequest(
                    id=1, money=amount, dest=1, interface=inter
                )
            )

    def Transfer(self, request, context):
        if self.balance >= request.money:
            dest_branch_id = request.dest
            dest_branch_stub = self.get_branch_stub(dest_branch_id)

        if dest_branch_stub:
            self.balance -= request.money
            dest_branch_stub.Deposit(
                project_pb2.MsgDeliveryRequest(
                    id=1, money=request.money, dest=dest_branch_id, interface="deposit"
                )
            )
            return project_pb2.MsgDeliveryReply(
                id=request.id, money=self.balance, result="success", interface=request.interface
            )
        return project_pb2.MsgDeliveryReply(
        id=request.id, money=self.balance, result="failure", interface=request.interface
    )
    def get_branch_stub(self, branch_id):
        for stub in self.stubList:
            if stub.GetBranchID() == branch_id:
                return stub
        return None

    def GetBranchID(self):
        return self.id

if __name__ == "__main__":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    this_port = int(sys.argv[1])
    branch_id = int(sys.argv[2])
    branch_balance = int(sys.argv[3])
    last_branch_port_plus_one = int(sys.argv[4])

    branches = list(range(1, last_branch_port_plus_one))
    branches.remove(branch_id)

    project_pb2_grpc.add_BankServicer_to_server(Branch(branch_id, branch_balance, branches), server)
    server.add_insecure_port(f"[::]:{this_port}")
    server.start()
    server.wait_for_termination()