from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    faceit_id = Column(String, unique=True, index=True)
    faceit_nickname = Column(String, index=True)
    steam_nickname = Column(String)
    avatar = Column(String)
    country = Column(String)

    stats = relationship('PlayerStats', uselist=False, backref='player')
    matches = relationship('Match', backref='player')

    def __repr__(self):
        return f'{self.faceit_nickname} - {self.faceit_id}'


class PlayerStats(Base):
    __tablename__ = 'players_stats'

    id = Column(Integer, primary_key=True)
    matches_count = Column(Integer)
    wins_count = Column(Integer)
    winrate = Column(Integer)
    rounds_count = Column(Integer)
    avg_kd = Column(Float)
    avg_kills = Column(Integer)
    avg_hs_percent = Column(Integer)
    hs_count = Column(Integer)
    kills_count = Column(Integer)
    deaths_count = Column(Integer)
    single_kills = Column(Integer)
    double_kills = Column(Integer)
    triple_kills = Column(Integer)
    quadro_kills = Column(Integer)
    aces = Column(Integer)
    mvps = Column(Integer)
    avg_kpr = Column(Float)
    avg_spr = Column(Float)
    avg_rmk = Column(Float)

    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)

    def __repr__(self):
        return f'Stats for player {self.player.faceit_nickname}'


class Match(Base):
    __tablename__ = 'matches'

    id = Column(Integer, primary_key=True)
    match_id = Column(String, index=True)
    map = Column(String)
    rounds = Column(Integer)
    kills = Column(Integer)
    deaths = Column(Integer)
    kd = Column(Float)
    kr = Column(Float)
    sr = Column(Float)
    single_kills = Column(Integer)
    double_kills = Column(Integer)
    triple_kills = Column(Integer)
    quadro_kills = Column(Integer)
    aces = Column(Integer)
    rating_1 = Column(Float)
    mvps = Column(Integer)
    hs_count = Column(Integer)
    hs_percent = Column(Integer)

    player_id = Column(Integer, ForeignKey('players.id'), nullable=False)

    def __repr__(self):
        return f'Match id: {self.match_id} | Player: {self.player.faceit_nickname}'











