from fsm import MooreMachine, State

parking_meter = MooreMachine('Parking Meter')

ready = State('Ready', initial=True)
verify = State('Verify')
await_action = State(r'Await\naction')
print_tkt = State('Print ticket')
return_money = State(r'Return\nmoney')
reject = State('Reject coin')

ready[r'coin inserted'] = verify

verify.update({'valid': State(r'add value\rto ticket'), 
               'invalid': reject})

for coin_value in verify:
    verify[coin_value][''] = await_action

await_action.update({'print': print_tkt,
                     'coin': verify,
                     'abort': return_money,
                     'timeout': return_money})

return_money[''] = print_tkt[''] = ready
