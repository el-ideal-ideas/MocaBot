insert into `[el]#moca_prefix#chat_logs`(
  ip, bot_id, user_msg, bot_msg, time, res_type, client_id
) values (%s, %s, %s, %s, %s, now(), %s);