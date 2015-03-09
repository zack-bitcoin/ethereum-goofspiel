import bitcoin as b
from pyethereum import utils

def hash_list(l):
    def g(x):
        if type(x) in [int, long]: x=utils.int_to_big_endian(x)
        return x
    y=map(g, l)
    y=[utils.zpad(x, 32) for x in y]
    y=''.join(y)
    #save for pretty print z="".join("{:02x}".format(ord(c)) for c in y)
    return b.sha256(y)
def mk_acc(n):
    out={"priv":b.sha256("brainwallet"+str(n))}
    out["pub"]=b.privtopub(out["priv"])
    out["addr"]=int(utils.privtoaddr(out["priv"]), 16)
    return(out)
def mk_sig(hash, priv): return list(b.ecdsa_raw_sign(hash, priv))
def mk_mk_sig(msghash): return (lambda p: mk_sig(msghash, p["priv"]))
def end_game(c, accs):
    h=hash_list([0, 0])
    sig1=mk_sig(h, accs[0]["priv"])
    sig2=mk_sig(h, accs[1]["priv"])
    c.end_game(0, sig1, sig2, accs[0]["addr"], accs[1]["addr"], 0)
def test(c):
    accs=[mk_acc(0), mk_acc(1)]
    #hash=#cards_per_suit, game_id, time_limit, bet, addr1, addr2
    c.deposit(accs[0]["addr"], value=1000)
    c.deposit(accs[1]["addr"], value=1000)
    h=hash_list([13, 0, 10, 100, accs[0]["addr"], accs[1]["addr"]])
    sig1=mk_sig(h,accs[0]["priv"])
    sig2=mk_sig(h,accs[1]["priv"])
    c.new_game(13, 0, 10, 100, accs[0]["addr"], accs[1]["addr"], sig1, sig2)
    hand=8191
    hand1=8190#played ace
    hand2=8175#played 5
    deck=8183#4 on top
    points1=0
    points2=4
    turn_nonce=1
    cards_per_hand=12
    game_id=0
    h=hash_list([cards_per_hand, game_id, accs[0]["addr"], accs[1]["addr"], hand1, hand2, points1, points2, turn_nonce, deck])
    sig1=mk_sig(h,accs[0]["priv"])
    sig2=mk_sig(h,accs[1]["priv"])
    card1=2
    card2=7
    salt1=12
    salt2=14
    commit_hash_1=hash_list([card1, salt1])
    commit_hash_2=hash_list([card2, salt2])
    old_salt1=55
    old_salt2=27
    print(sig1)
    print("sig2: " +str(sig2))
    print(game_id)
    print(hand1)
    print(hand2)
    print(points1)
    print(points2)
    print(turn_nonce)
    print(deck)
    print(cards_per_hand)
    print(commit_hash_1)
    print(commit_hash_2)
    print(utils.big_endian_to_int(commit_hash_1))
    print(utils.big_endian_to_int(commit_hash_2))
    c.poly_commit(sig1, sig2, game_id, hand1, hand2, points1, points2, turn_nonce, deck, cards_per_hand, utils.big_endian_to_int(commit_hash_1), utils.big_endian_to_int(commit_hash_2), old_salt1, old_salt2)
    #end_game(c, accs)
    print(c.check_balance(accs[0]["addr"]))
    print(c.check_balance(accs[1]["addr"]))
