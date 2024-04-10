#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import logging
import os
import random
import sys
from web3 import Web3

logging.basicConfig(level=logging.INFO)


FOLDER_PATH = os.path.dirname(os.path.realpath(__file__))


def shuffle_list_with_seed(wallet_address_list, seed_phrase):
    random.seed(seed_phrase)
    shuffled_list = wallet_address_list[:]
    random.shuffle(shuffled_list)
    return shuffled_list


def is_valid_eth_address(address):
    try:
        web3 = Web3()
        return web3.is_address(address)
    except ValueError:
        return False


def to_checksum_address(address):
    web3 = Web3()
    return web3.to_checksum_address(address)


def read_task_master_pool():
    file_path = f"{FOLDER_PATH}/task_master_prize_eligible_wallets.csv"
    wallet_address_list = []
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            wallet_address_list.extend(row)
    return wallet_address_list


def output_task_master_prize_result(wallet_address_lxp):
    file_path = f"{FOLDER_PATH}/task_master_prize_results.csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["wallet_address", "lxp_point"])
        writer.writerows(wallet_address_lxp)


def read_jackpot_bonus_pool():
    file_path = f"{FOLDER_PATH}/jackpot_bonus_prize_eligible_wallets.csv"
    wallet_address_list = []
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            wallet_address_list.extend(row)
    return wallet_address_list


def output_jackpot_bonus_result(wallet_address_prize):
    file_path = f"{FOLDER_PATH}/jackpot_bonus_prize_results.csv"
    with open(file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["wallet_address", "prize"])
        writer.writerows(wallet_address_prize)


def read_jackpot_bonus_prize():
    file_path = f"{FOLDER_PATH}/jackpot_bonus_prize.csv"
    prize_list = []
    with open(file_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            prize_list.append(row)
    return prize_list


def run_task_master_prize(seed_phrase):
    logging.info("Start to run task master prize pool")
    wallet_address_list = read_task_master_pool()
    logging.info("Read %s wallet addresses", len(wallet_address_list))

    # Iterate and make sure all addresses are valid
    logging.info("Clean up wallet addresses")
    clean_wallet_address_list = []
    for address in wallet_address_list:
        if address:
            clean_wallet_address_list.append(address.lower())
    clean_wallet_address_list = sorted(clean_wallet_address_list)
    logging.info(
        "After clean up, there are %s wallet addresses", len(clean_wallet_address_list)
    )

    # Run random shuffle based on seed_phrase
    logging.info("Ordering wallet addreses based on seed phrase '%s'", seed_phrase)
    shuffled_wallet_address_list = shuffle_list_with_seed(
        clean_wallet_address_list, seed_phrase
    )

    # Now assign prize by this list order
    logging.info("Starting to assign prize based on the wallet list order")
    wallet_address_lxp = []
    for i in range(len(shuffled_wallet_address_list)):
        if i < len(shuffled_wallet_address_list) * 0.55:
            wallet_address_lxp.append([shuffled_wallet_address_list[i], 150])
        elif (
            i >= len(shuffled_wallet_address_list) * 0.55
            and i < len(shuffled_wallet_address_list) * 0.8
        ):
            wallet_address_lxp.append([shuffled_wallet_address_list[i], 200])
        elif (
            i >= len(shuffled_wallet_address_list) * 0.8
            and i < len(shuffled_wallet_address_list) * 0.95
        ):
            wallet_address_lxp.append([shuffled_wallet_address_list[i], 225])
        else:
            wallet_address_lxp.append([shuffled_wallet_address_list[i], 250])

    logging.info("Complete! Now output the task master prize results..")
    output_task_master_prize_result(wallet_address_lxp)


def run_jackpot_bonus_prize(seed_phrase):
    logging.info("Start to run task master prize pool")
    wallet_address_list = read_jackpot_bonus_pool()
    logging.info("Read %s wallet addresses", len(wallet_address_list))
    jackpot_bonus_prize_list = read_jackpot_bonus_prize()
    logging.info("Read %s prizes from the jackpot pool", len(jackpot_bonus_prize_list))

    # Iterate and make sure all addresses are valid
    logging.info("Clean up wallet addresses")
    clean_wallet_address_list = []
    for address in wallet_address_list:
        if address:
            clean_wallet_address_list.append(address.lower())
    clean_wallet_address_list = sorted(clean_wallet_address_list)
    logging.info(
        "After clean up, there are %s wallet addresses", len(clean_wallet_address_list)
    )

    # Run random shuffle based on seed_phrase
    logging.info("Ordering wallet addreses based on seed phrase '%s'", seed_phrase)
    shuffled_wallet_address_list = shuffle_list_with_seed(
        clean_wallet_address_list, seed_phrase
    )

    # calculate prize and winner index
    logging.info("Starting to assign prize based on the wallet list order")
    wallet_address_prize = []
    for prize, num_winners in jackpot_bonus_prize_list:

        # Select winners
        winners = shuffled_wallet_address_list[: int(num_winners)]

        # Record distributed prizes
        for winner in winners:
            wallet_address_prize.append([winner, prize])

        # Remove winners from user list
        shuffled_wallet_address_list = shuffled_wallet_address_list[int(num_winners) :]

    for wallet in shuffled_wallet_address_list:
        wallet_address_prize.append([wallet, ''])

    logging.info("Complete! Now output the jackpot bonus prize results..")
    output_jackpot_bonus_result(wallet_address_prize)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        logging.error("Please provide 2 seed phrases")
        exit(0)

    # Run task master price
    # Random LXP drop within the range of [150] LXP to [250] LXP for Linea park participants that completing 70% basic tasks in the park.
    # LXP allocation through raffle
    # 150 LXP: 55% of participants
    # 200 LXP: 25% of participants
    # 225 LXP: 15% of participants
    # 250 LXP: 5% of participants
    # We will randomly shuffle the list and the first 55% wallets win 150 LXP, next 25% wallets win 200 LXP.
    # Then next 15% win 225 LXP and last 5% win 250 LXP
    run_task_master_prize(sys.argv[1])

    # projects all together contribute two categories of prize
    # one that all eligible participants will get
    # the other are fixed amount of prized for the raffle
    # We will distribute the fixed amount of prize in this function
    run_jackpot_bonus_prize(sys.argv[2])
