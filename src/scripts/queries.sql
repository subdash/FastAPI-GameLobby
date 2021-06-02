-- Project email, time_avail and game name
select user.email, availability.time_avail, game.name
from user
inner join availability on user.id = availability.user_id
inner join interest on user.id = interest.user_id
inner join game on game.id = interest.game_id;
