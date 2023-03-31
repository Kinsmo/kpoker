import itertools
from collections import Counter
import numpy as np
from kinspy.print_functions import *
import streamlit as st

def make_poker():
    numbers = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    suits = [1,2,3,4]
    Pokers = [[number,suit] for number in numbers for suit in suits]
    return Pokers

def print_poker(Pokers):
    value_map = {2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:'J',12:'Q',13:'K',14:'A'}
    suit_map = {1:'\u2660',2:':red[\u2665]',3:'\u2663',4:':red[\u2666]'}
    s = ""
    for poker in Pokers:
        s+=f"{value_map[poker[0]]}{suit_map[poker[1]]} "
    st.title(f"{s}")

def is_flush(hand_cards):
    return all([poker[1] == hand_cards[0][1] for poker in hand_cards])

def compare_flush(all_flush_cards):
    powers = [max(flush_cards[:,0]) for flush_cards in all_flush_cards]
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_straight(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    values.sort()
    return (all([not bool(values[i+1] - values[i] - 1) for i in range(4)]))

def compare_straight(all_straight_cards):
    return compare_flush(all_straight_cards)

def is_straight_flush(hand_cards):
    return is_straight(hand_cards) and is_flush(hand_cards)

def compare_straight_flush(all_straight_cards):
    return compare_flush(all_straight_cards)

def is_four(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    if values.count(hand_cards[0][0]) == 4 or values.count(hand_cards[1][0]) == 4:
        return True

def compare_four(all_straight_cards):
    powers = []
    for hand_cards in all_straight_cards:
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_count = {y:x for x,y in value_count.items()}
        power = value_count[4]*100 + value_count[1]
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_three(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    value_count =  dict(Counter(values))
    counts = [y for x,y in value_count.items()]
    if 3 in counts and not 2 in counts:
        return True

def compare_three(all_cards):
    powers = []
    for hand_cards in all_cards:
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_three = max([x for x,y in value_count.items() if y==3])
        value_single = max([x for x,y in value_count.items() if y==1])
        power = value_three*100 + value_single
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_house(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    value_count =  dict(Counter(values))
    counts = [y for x,y in value_count.items()]
    if 3 in counts and 2 in counts:
        return True 

def compare_house(all_cards):
    powers = []
    for hand_cards in all_cards:
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_count = {y:x for x,y in value_count.items()}
        power = value_count[3]*100 + value_count[2]
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_two_pair(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    value_count =  dict(Counter(values))
    counts = [y for x,y in value_count.items()]
    sets = set(values)
    if len(sets) == 3 and 2 in counts:
        return True 

def compare_two_pair(all_cards):
    powers = []
    for hand_cards in all_cards:
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_two1 = max([x for x,y in value_count.items() if y==2])
        value_two2 = min([x for x,y in value_count.items() if y==2])
        value_single = max([x for x,y in value_count.items() if y==1])
        power = value_two1*100 + value_two2 + value_single*0.01
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_high(hand_cards):
    values = list(np.array(hand_cards)[:,0])
    sets = set(values)
    if len(sets) == 5 and not is_straight(hand_cards):
        return True 
    
def compare_high(all_cards):
    powers = []
    for hand_cards in all_cards:
        power = max(list(np.array(hand_cards)[:,0]))
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_pair(hand_cards):
    n = set([poker[0] for poker in hand_cards])
    if len(n) == 4 and not is_flush(hand_cards):
        return True   

def compare_pair(all_cards):
    powers = []
    for hand_cards in all_cards:
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_two = max([x for x,y in value_count.items() if y==2])
        value_single = max([x for x,y in value_count.items() if y==1])
        power = value_two*100 + value_single
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def is_royal_flush(hand_cards):
    if is_straight_flush(hand_cards) and 'A' in [card[0] for card in hand_cards]:
        return True

def compare_royal_flush(all_straight_cards):
    return compare_flush(all_straight_cards)
   
def compare_flush(all_flush_cards):
    flush_powers = [max(flush_cards[:,0]) for flush_cards in all_flush_cards]
    max_power = max(flush_powers)
    winners = [i for i,x in enumerate(flush_powers) if x == max_power]
    return winners


def check_hand_cards(hand_cards):
    if is_high(hand_cards): 
        power = 1*10000 + max(list(np.array(hand_cards)[:,0]))
        return 1,power
    
    if is_pair(hand_cards): 
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_two = max([x for x,y in value_count.items() if y==2])
        value_single = max([x for x,y in value_count.items() if y==1])
        power = 2*10000 + value_two*100 + value_single
        return 2,power
    
    if is_two_pair(hand_cards): 
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_two1 = max([x for x,y in value_count.items() if y==2])
        value_two2 = min([x for x,y in value_count.items() if y==2])
        value_single = max([x for x,y in value_count.items() if y==1])
        power = 3*10000 + value_two1*100 + value_two2 + value_single*0.01
        return 3,power
    
    if is_three(hand_cards): 
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_three = max([x for x,y in value_count.items() if y==3])
        value_single1 = max([x for x,y in value_count.items() if y==1])
        value_single2 = min([x for x,y in value_count.items() if y==1])
        power = 4*10000 + value_three*100 + value_single1 + value_single2*0.01
        return 4,power
    
    if is_straight(hand_cards): 
        power = 5*10000 + max(list(np.array(hand_cards)[:,0]))
        return 5,power
    
    if is_flush(hand_cards): 
        power = 6*10000 + max(list(np.array(hand_cards)[:,0]))
        return 6,power
    
    if is_house(hand_cards): 
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_count = {y:x for x,y in value_count.items()}
        power = 7*10000 + value_count[3]*100 + value_count[2]
        return 7,power
    
    if is_four(hand_cards): 
        values = list(np.array(hand_cards)[:,0])
        value_count = dict(Counter(values))
        value_count = {y:x for x,y in value_count.items()}
        power = 8*10000 + value_count[4]*100 + value_count[1]
        return 8,power
    
    if is_straight_flush(hand_cards): 
        power = 9*10000 + max(list(np.array(hand_cards)[:,0]))
        return 9,power
    
    if is_royal_flush(hand_cards): 
        power = 10*10000 + max(list(np.array(hand_cards)[:,0]))
        return 10,power
    
    st.write("No Type Match")
    print_poker(hand_cards)

def check_winners(all_cards):
    powers = []
    for hand_cards in all_cards:
        x,power = check_hand_cards(hand_cards)
        powers.append(power)
    max_power = max(powers)
    winners = [i for i,x in enumerate(powers) if x == max_power]
    return winners

def popn(Remain_Pokers,n):
    if n==1: return Remain_Pokers.pop(0)
    return [Remain_Pokers.pop(0) for i in range(n)]

def hit_cards(cards7):
    comb_hand_cards = list(itertools.combinations(cards7, 5))
    powers = [check_hand_cards(hand_cards)[1] for hand_cards in comb_hand_cards]
    power = max(powers)
    kind = power // 10000
    index = [i for i in range(len(powers)) if powers[i] == power][0]
    card = comb_hand_cards[index]
    return kind, power, card

def judge_two(my_poker,enemy_poker,public_poker):
    kind_map = {1:'high',2:'pair',3:'two pair',4:'three',5:'straight',6:'flush',7:'house',8:'four',9:'straight flush',10:'royal flush'}
    cards7 = my_poker + public_poker
    kind1,power1,card1 = hit_cards(cards7)
    kind1 = kind_map[kind1]

    cards7 = enemy_poker + public_poker
    kind2,power2,card2 = hit_cards(cards7)
    kind2 = kind_map[kind2]

    st.write(f"Your Hit:{kind1}")
    print_poker(card1)
    st.write(f"Enemy Hit:{kind2}")
    print_poker(card2)

    if power1 > power2:
        st.write("YOU WIN!!!")
    if power1 < power2:
        st.write("YOU LOSE!!!")
    if power1 == power2:
        st.write("SAME!!!")

def judge(my_poker,enemy_pokers,public_poker,all_in = False):
    kind_map = {1:'high',2:'pair',3:'two pair',4:'three',5:'straight',6:'flush',7:'house',8:'four',9:'straight flush',10:'royal flush'}
    cards7 = my_poker + public_poker
    kind1,power1,card1 = hit_cards(cards7)
    kind1 = kind_map[kind1]

    power2s = []
    card2s = []
    kind2s = []
    for enemy_poker in enemy_pokers:
        cards7 = enemy_poker + public_poker
        kind2,power2,card2 = hit_cards(cards7)
        power2s.append(power2)
        card2s.append(card2)
        kind2s.append(kind2)
    power2 = max(power2s)

    winners = [i for i,x in enumerate(power2s) if x == power2]
    enemy_winner = winners[0]
    card2 = card2s[enemy_winner]
    kind2 = kind_map[kind2]

    if len(winners) >1: st.write("Many Enemy Winners!!!")

    st.title(f":blue[**You Hit: {kind1}**]")
    print_poker(card1)
    st.title(f":red[**Enemy Hit: {kind2}**]")
    print_poker(card2)

    if power1 >= power2:
        if all_in:
            st.sucess("YOU WIN!!!")
            st.balloons()
        else:
            st.warning("BAD DECISION!!!")
            st.snow()
    if power1 < power2:
        if all_in:
            st.error("YOU LOSE!!!")
            st.snow()
        else:
            st.success("GOOD DECISION!!!")
            st.balloons()

def print_poker_all(all_pokers):
    for pokers in all_pokers:
        print_poker(pokers)
