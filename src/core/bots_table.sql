create table if not exists `%sbots` (
    bot_id bigint auto_increment primary key,
    bot_name varchar(128) unique not null
)engine=innodb default charset = utf8mb4;