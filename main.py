import random
from kpoker import *
from kinspy.print_functions import *
import streamlit as st

st.title("Kpoker")
col1,col2 = st.columns(2)

# "01 New Cards"
Pokers = make_poker()

# "02 Shuffle Cards"
random.shuffle(Pokers)

# "03 Your Poker"
my_poker = popn(Pokers,2)

# "04 Enemy Poker"
n_enemy = st.number_input("Number of Players:", value = 5)

enemy_pokers = [popn(Pokers,2) for i in range(n_enemy)]

# "05 Public Poker"
public_poker = 0

# "06 Look Poker"
with col2:
    print_poker(my_poker)
    is_call = st.button("ALL IN")
    is_drop = st.button("DROP")

with col1:
    # "07 Start Playing"
    for i in [2,5,6,7]:
        if is_drop and i==2:
            print_poker_all(enemy_pokers)
            break

        if is_drop and i in [5,6,7]:
            judge(my_poker,enemy_pokers,public_poker)
            break

    #         "Flop"
        if is_call and i ==2:
            public_poker = popn(Pokers,3)
            print_poker(public_poker)

    #         "Turn"
        if is_call and i ==5:
            public_poker.append(popn(Pokers,1))
            print_poker(public_poker)

    #         "River"
        if is_call and i ==6:
            public_poker.append(popn(Pokers,1))
            print_poker(public_poker)

    #         "All In"
        if is_call and i ==7:
            judge(my_poker,enemy_pokers,public_poker,all_in = True)
