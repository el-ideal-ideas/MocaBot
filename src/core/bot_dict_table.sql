create table if not exists `%sbot_dict` (
    id bigint auto_increment primary key,
    bot_id bigint not null,
    text varchar(2048) not null,
    foreign key (bot_id) references `%sbots` (bot_id)
)engine=innodb default charset = utf8mb4;