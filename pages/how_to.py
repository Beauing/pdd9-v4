import streamlit as st

def main():
    st.header("Log Event Components")

    st.subheader("Kill")
    st.code(r"\x08 \x08Kill: 6 1 4: Player_172.19.117.18 killed Player_172.19.137.208 by MOD_GRENADE")
    st.text("""
    (prefix) (attacker_id) (victim_id) (weapon_id) (attacker_ip_name) (victim_ip_name) (weapon_name)
        •	prefix: \x08 \x08Kill:
        •	attacker_id: 6
        •	victim_id: 1
        •	weapon_id: 4
        •	attacker: Player_172.19.117.18
        •	victim: Player_172.19.137.208
        •	weapon: MOD_GRENADE
    """)

    st.subheader("PlayerScore")
    st.code(r"\x08 \x08PlayerScore: 6 1: Player_172.19.117.18 now has 1 points")
    st.text("""
    (prefix) (player_id) (score) (player) (points)
        •	prefix: \x08 \x08PlayerScore:
        •	player_id: 6
        •	score: 1
        •	player: Player_172.19.117.18
        •	points: 1
    """)

    st.subheader("Challenge")
    st.code(r"\x08 \x08Challenge: 6 402 1: Client 6 got award 402")
    st.text("""
    (prefix) (client_id) (award_id) (count) (client) (award)
        •	prefix: \x08 \x08Challenge:
        •	client_id: 6
        •	award_id: 402
        •	count: 1
        •	client: Client 6
        •	award: 402
    """)

    st.subheader("Award")
    st.code(r"\x08 \x08Award: 2 1: Player_172.19.114.48 gained the EXCELLENT award!\n")
    st.text("""
    (prefix) (player_id) (award_id) (player) (award)
        •	prefix: \x08 \x08Award:
        •	player_id: 2
        •	award_id: 1
        •	player: Player_172.19.114.48
        •	award: EXCELLENT award
    """)

    st.header("Client Number Assignment")
    st.write("""
    - Client `1`: Player_172.19.137.208
    - Client `2`: Player_172.19.114.48
    - Client `3`: Player_172.19.119.51
    - Client `4`: Player_172.19.116.18
    - Client `5`: Player_172.19.120.104
    - Client `6`: Player_172.19.117.18
    """)

    st.header("Dataframe Headers")
    st.write("""
    - `timestamp`: The exact time when the event occurred.
    - `event`: Type of event (e.g., Kill, PlayerScore, Challenge).
    - `killer_id`: ID of the player who made the kill (for Kill events).
    - `victim_id`: ID of the player who was killed (for Kill events).
    - `weapon_id`: ID of the weapon used (for Kill events).
    - `killer_ip`: IP address of the player who made the kill.
    - `victim_ip`: IP address of the player who was killed.
    - `weapon`: Type of weapon used (for Kill events).
    - `player_id`: ID of the player involved in the event.
    - `score`: Score of the player (for PlayerScore events).
    - `player_ip`: IP address of the player (for PlayerScore events).
    - `award_id`: ID of the award given (for Challenge events).
    """)

    st.header("Maps")
    st.write("""
    - `kaos2`: break round, enclosed arena
    - `aggressor`: indoor map, players can die from lava (MOD_LAVA)
    - `wrackdm17`: outdoor map, players can fall to their death (MOD_FALLING)
    """)

    st.header("Types of weapons and IDs")
    st.write("""
    - MOD_SHOTGUN: `1`
    - MOD_GAUNTLET: `2`
    - MOD_MACHINEGUN: `3`
    - MOD_GRENADE: `4`
    - MOD_GRENADE_SPLASH: `5`
    - MOD_ROCKET: `6`
    - MOD_ROCKET_SPLASH: `7`
    - MOD_PLASMA: `8`
    - MOD_PLASMA_SPLASH: `9`
    - MOD_RAILGUN: `10`
    - MOD_LIGHTNING: `11`
    - MOD_LAVA: `16`
    - MOD_TELEFRAG: `18`
    - MOD_FALLING: `19`
    - MOD_SUICIDE: `20`
    - MOD_TRIGGER_HURT: `22`
    """)

main()
