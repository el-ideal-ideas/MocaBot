create table if not exists `%sbot_dict` (
    id bigint auto_increment primary key,
    bot_id bigint not null,
    text varchar(512) not null,
    foreign key (bot_id) references `%sbots` (bot_id)
);