create table if not exists `%schat_logs` (
    id bigint auto_increment primary key,
    ip varchar(256) not null,
    bot_id bigint not null,
    user_msg varchar(2048) not null,
    bot_msg varchar(2048) not null,
    time datetime not null,
    res_type varchar(64) not null,
    client_id varchar(256) default null,
    foreign key (bot_id) references `%sbots` (bot_id)
)engine=innodb default charset = utf8mb4;