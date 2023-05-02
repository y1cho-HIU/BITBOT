import params_private as prv
import params_public as pub


def calc_rrr(env, sma, rate):
    return round(((rate + 1) * env - sma) / rate, 4)


def strategy(now_price, sma_list, now_pos, env_weight):
    signal = False
    next_pos = now_pos
    now_sma = round(sum(sma_list)/len(sma_list), 4)
    env_up = round(now_sma * (1 + env_weight), 4)
    env_down = round(now_sma * (1 - env_weight), 4)
    rrr_up = calc_rrr(env=env_up, sma=now_sma, rate=prv.rrr_rate)
    rrr_down = calc_rrr(env=env_down, sma=now_sma, rate=prv.rrr_rate)

    if now_pos == pub.POS_OUT:
        if now_price <= env_down:
            # pos 진입 시, 가격도 return
            next_pos = pub.POS_LONG
            signal = True

        if now_price >= env_up:
            # pos 진입 시, 가격도 return
            next_pos = pub.POS_SHORT
            signal = True

    elif now_pos == pub.POS_LONG:
        if (now_price >= now_sma) | (now_price <= rrr_down):
            # now_price <-> pos_in price 비교 후 win/lose 판단
            next_pos = pub.POS_OUT
            signal = True

    elif now_pos == pub.POS_SHORT:
        if (now_price <= now_sma) | (now_price >= rrr_up):
            # now_price <-> pos_in price 비교 후 win/lose 판단
            next_pos = pub.POS_OUT
            signal = True

    return next_pos, signal
