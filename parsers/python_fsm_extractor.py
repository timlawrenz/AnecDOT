#!/usr/bin/env python3
"""
Quick extractor for oozie/python-fsm README examples.
Manually extracts the 3 well-documented examples.
"""

import sys
from pathlib import Path

# Add python-fsm to path
sys.path.insert(0, "/tmp/python-fsm/src")

from fsm import FiniteStateMachine, get_graph, State, MooreMachine, MealyMachine

output_dir = Path("/home/tim/source/activity/AnecDOT/data/raw/python_fsm_extraction")
output_dir.mkdir(parents=True, exist_ok=True)

def save_example(name, description, code, fsm_obj):
    """Save example with code and DOT."""
    pair_dir = output_dir / name
    pair_dir.mkdir(exist_ok=True)
    
    (pair_dir / "description.txt").write_text(description)
    (pair_dir / "code.py").write_text(code)
    
    # Get DOT
    graph = get_graph(fsm_obj)
    dot = graph.to_string()
    (pair_dir / "diagram.dot").write_text(dot)
    
    metadata = f"""Source: oozie/python-fsm README
Type: {type(fsm_obj).__name__}
Description: {description}
"""
    (pair_dir / "metadata.txt").write_text(metadata)
    print(f"✓ Saved {name}")

# Example 1: TCP/IP
print("Extracting TCP/IP state machine...")
tcpip_code = """from fsm import FiniteStateMachine, State

STATES = ['LISTEN', 'SYN RCVD', 'ESTABLISHED', 'SYN SENT', 
          'FIN WAIT 1', 'FIN WAIT 2', 'TIME WAIT', 'CLOSING', 'CLOSE WAIT',
          'LAST ACK']

tcpip = FiniteStateMachine('TCP IP')

closed = State('CLOSED', initial=True)
listen, synrcvd, established, synsent, finwait1, finwait2, timewait, \\
closing, closewait, lastack = [State(s) for s in STATES]

timewait['(wait)'] = closed
closed.update({r'passive\\nopen': listen,
               'send SYN': synsent})

synsent.update({r'close /\\ntimeout': closed,
                r'recv SYN,\\nsend\\nSYN+ACK': synrcvd,
                r'recv SYN+ACK,\\nsend ACK': established})

listen.update({r'recv SYN,\\nsend\\nSYN+ACK': synrcvd,
               'send SYN': synsent})

synrcvd.update({'recv ACK': established,
                'send FIN': finwait1,
                'recv RST': listen})

established.update({'send FIN': finwait1,
                    r'recv FIN,\\nsend ACK': closewait})

closewait['send FIN'] = lastack

lastack['recv ACK'] = closed

finwait1.update({'send ACK': closing,
                 'recv ACK': finwait2,
                 r'recv FIN, ACK\\n send ACK': timewait})

finwait2[r'recv FIN,\\nsend ACK'] = timewait

closing[r'recv\\nACK'] = timewait
"""

tcpip = FiniteStateMachine('TCP IP')
closed = State('CLOSED', initial=True)
STATES = ['LISTEN', 'SYN RCVD', 'ESTABLISHED', 'SYN SENT', 
          'FIN WAIT 1', 'FIN WAIT 2', 'TIME WAIT', 'CLOSING', 'CLOSE WAIT',
          'LAST ACK']
listen, synrcvd, established, synsent, finwait1, finwait2, timewait, \
closing, closewait, lastack = [State(s) for s in STATES]

timewait['(wait)'] = closed
closed.update({r'passive\nopen': listen, 'send SYN': synsent})
synsent.update({r'close /\ntimeout': closed,
                r'recv SYN,\nsend\nSYN+ACK': synrcvd,
                r'recv SYN+ACK,\nsend ACK': established})
listen.update({r'recv SYN,\nsend\nSYN+ACK': synrcvd, 'send SYN': synsent})
synrcvd.update({'recv ACK': established, 'send FIN': finwait1, 'recv RST': listen})
established.update({'send FIN': finwait1, r'recv FIN,\nsend ACK': closewait})
closewait['send FIN'] = lastack
lastack['recv ACK'] = closed
finwait1.update({'send ACK': closing, 'recv ACK': finwait2,
                 r'recv FIN, ACK\n send ACK': timewait})
finwait2[r'recv FIN,\nsend ACK'] = timewait
closing[r'recv\nACK'] = timewait

save_example("tcpip", "TCP/IP state transitions implementing connection lifecycle", 
             tcpip_code, tcpip)

# Example 2: Parking Meter
print("Extracting Parking Meter state machine...")
parking_code = """from fsm import MooreMachine, State

parking_meter = MooreMachine('Parking Meter')

ready = State('Ready', initial=True)
verify = State('Verify')
await_action = State(r'Await\\naction')
print_tkt = State('Print ticket')
return_money = State(r'Return\\nmoney')
reject = State('Reject coin')

ready[r'coin inserted'] = verify

verify.update({'valid': State(r'add value\\rto ticket'), 
               'invalid': reject})

for coin_value in verify:
    verify[coin_value][''] = await_action

await_action.update({'print': print_tkt,
                     'coin': verify,
                     'abort': return_money,
                     'timeout': return_money})

return_money[''] = print_tkt[''] = ready
"""

parking_meter = MooreMachine('Parking Meter')
ready = State('Ready', initial=True)
verify = State('Verify')
await_action = State(r'Await\naction')
print_tkt = State('Print ticket')
return_money = State(r'Return\nmoney')
reject = State('Reject coin')
ready[r'coin inserted'] = verify
verify.update({'valid': State(r'add value\rto ticket'), 'invalid': reject})
for coin_value in verify:
    verify[coin_value][''] = await_action
await_action.update({'print': print_tkt, 'coin': verify,
                     'abort': return_money, 'timeout': return_money})
return_money[''] = print_tkt[''] = ready

save_example("parking_meter", 
             "Dublin City Council parking meter (Moore Machine) for coin-operated ticket system",
             parking_code, parking_meter)

# Example 3: Binary Adder
print("Extracting Binary Adder state machine...")
adder_code = """from fsm import MealyMachine, State

adder = MealyMachine('Binary addition')

carry = State('carry')
nocarry = State('no carry', initial=True)

nocarry[(1, 0), 1] = nocarry
nocarry[(0, 1), 1] = nocarry
nocarry[(0, 0), 0] = nocarry
nocarry[(1, 1), 0] = carry

carry[(1, 1), 1] = carry
carry[(0, 1), 0] = carry
carry[(1, 0), 0] = carry
carry[(0, 0), 1] = nocarry
"""

adder = MealyMachine('Binary addition')
carry = State('carry')
nocarry = State('no carry', initial=True)
nocarry[(1, 0), 1] = nocarry
nocarry[(0, 1), 1] = nocarry
nocarry[(0, 0), 0] = nocarry
nocarry[(1, 1), 0] = carry
carry[(1, 1), 1] = carry
carry[(0, 1), 0] = carry
carry[(1, 0), 0] = carry
carry[(0, 0), 1] = nocarry

save_example("binary_adder",
             "Binary adder (Mealy Machine) implementing single-bit addition with carry",
             adder_code, adder)

print("\n" + "="*70)
print("Extracted 3 pairs from oozie/python-fsm")
print("="*70)
