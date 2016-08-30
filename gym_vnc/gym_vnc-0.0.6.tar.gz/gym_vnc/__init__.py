import gym
import logging
import os
import sys
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# Should be exactly the same as CartPole-v0
register(
    id='VNCCartPoleLowDSync-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    kwargs={
        'vnc_pixels': False,
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=100,
)

# Async cartpole with 4-d observations
register(
    id='VNCCartPoleLowD-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
    kwargs={
        'vnc_pixels': False,
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=100,
)

register(
    id='VNCCartPole-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
    kwargs={
        'core_env_id': 'CartPole-v0',
    },
    # experience_limit=1000,
    trials=2,
    timestep_limit=100,
)

register(
    id='PongShortSync-v0',
    entry_point='gym_vnc.envs.short_env:ShortEnv',
    kwargs={
        'timestep_limit': 10,
        'env_entry_point': 'gym.envs.atari:AtariEnv',
        'env_kwargs': {
            'game': 'pong', 'obs_type': 'image'
        }
    },
)

register(
    id='VNCPongShortSync-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    kwargs={
        'core_env_id': 'PongShortSync-v0',
    }
)

register(
    id='PitfallShortSync-v0',
    entry_point='gym_vnc.envs.short_env:ShortEnv',
    kwargs={
        'timestep_limit': 10,
        'env_entry_point': 'gym.envs.atari:AtariEnv',
        'env_kwargs': {
            'game': 'pitfall', 'obs_type': 'image'
        }
    },
)

register(
    id='VNCPitfallShortSync-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
    kwargs={
        'core_env_id': 'PitfallShortSync-v0',
    }
    # experience_limit=1000,
)

# VNCAtari
for game in ['air_raid', 'alien', 'amidar', 'assault', 'asterix',
             'asteroids', 'atlantis', 'bank_heist', 'battle_zone',
             'beam_rider', 'berzerk', 'bowling', 'boxing', 'breakout',
             'carnival', 'centipede', 'chopper_command', 'crazy_climber',
             'demon_attack', 'double_dunk', 'elevator_action', 'enduro',
             'fishing_derby', 'freeway', 'frostbite', 'gopher', 'gravitar',
             'ice_hockey', 'jamesbond', 'journey_escape', 'kangaroo', 'krull',
             'kung_fu_master', 'montezuma_revenge', 'ms_pacman',
             'name_this_game', 'phoenix', 'pitfall', 'pong', 'pooyan',
             'private_eye', 'qbert', 'riverraid', 'road_runner', 'robotank',
             'seaquest', 'skiing', 'solaris', 'space_invaders', 'star_gunner',
             'tennis', 'time_pilot', 'tutankham', 'up_n_down', 'venture',
             'video_pinball', 'wizard_of_wor', 'yars_revenge', 'zaxxon']:
    # space_invaders should yield SpaceInvaders-v0 and SpaceInvaders-ram-v0
    base = ''.join([g.capitalize() for g in game.split('_')]) # SpaceInvaders
    core_env_id = base + '-v0' # SpaceInvaders-v0
    register(
        id='VNC{}'.format(core_env_id),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
        kwargs={
            'core_env_id': core_env_id
        }
        # experience_limit=1000,
    )

    register(
        id='VNC{}Sync-v0'.format(base),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreSyncEnv',
        kwargs={
            'core_env_id': core_env_id,
        }
        # experience_limit=1000,
    )

    register(
        id='VNC{}30FPS-v0'.format(base),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
        kwargs={
            'core_env_id': core_env_id,
            'fps': 30,
        }
        # experience_limit=1000,
    )

    register(
        id='VNC{}Slow-v0'.format(base),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
        kwargs={
            'core_env_id': core_env_id,
            'fps': 15,
        }
        # experience_limit=1000,
    )

    deterministic_core_env_id = base + 'Deterministic-v0'  # SpaceInvadersDeterministic-v0

    register(
        id='VNC{}Deterministic-v0'.format(base),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
        kwargs={
            'core_env_id': deterministic_core_env_id,
        }
    )
    register(
        id='VNC{}DeterministicSlow-v0'.format(base),
        entry_point='gym_vnc.wrappers:WrappedVNCCoreEnv',
        kwargs={
            'core_env_id': deterministic_core_env_id,
            'fps': 15,
        }
    )

# VNCFlashgames

for game in ['VNC42Game-v0', 'VNCAirBattle-v0', 'VNCAmberialAxis-v0',
             'VNCAthletics-v0', 'VNCAvalancher-v0',
             'VNCAvatarElementalEscape-v0', 'VNCBowAdventure-v0', 'VNCCanopy-v0',
             'VNCCaveman-v0', 'VNCChronotron-v0', 'VNCCommunityCollegeSim-v0',
             'VNCDannyPhantom-v0', 'VNCDirkValentine-v0',
             'VNCDonkeyKongReturns-v0', 'VNCDoubleEdged-v0',
             'VNCEnoughPlumbers2-v0', 'VNCEscapeTheRedGiant-v0', 'VNCFat-v0',
             'VNCFinalCommando-v0', 'VNCFirebug-v0', 'VNCFlagman-v0',
             'VNCFloodRunner4-v0', 'VNCFlubberRise-v0', 'VNCFrogDares-v0',
             'VNCGSwitch-v0', 'VNCGravinaytor-v0', 'VNCGuitarManiac-v0',
             'VNCGunpowderAndFeathers-v0', 'VNCHeavyPawnage-v0',
             'VNCHelicopter-v0', 'VNCIndestructoTank-v0', 'VNCIndianaJones-v0',
             'VNCJamesTheCircusZebra-v0', 'VNCJamesTheSpaceZebra-v0',
             'VNCJetpacTheRemake-v0', 'VNCJimmyJumper-v0', 'VNCKillbot-v0',
             'VNCKillme-v0', 'VNCLeapOfFaith-v0', 'VNCLemmingsReturns-v0',
             'VNCLittleLoki-v0', 'VNCMalichite-v0', 'VNCMarioCatcher2-v0',
             'VNCMarioCombat-v0', 'VNCMarioTimeAttack-v0',
             'VNCMatrixBulletTime-v0', 'VNCMetroSiberia-v0', 'VNCMonkeyManic-v0',
             'VNCMonolithsMarioWorld2-v0', 'VNCMonsterEvolution-v0', 'VNCMoss-v0',
             'VNCMotherLoad-v0', 'VNCMultitask-v0', 'VNCNanowar-v0',
             'VNCNinjaCat-v0', 'VNCOfficeTrap-v0', 'VNCOneAndOneStory-v0',
             'VNCOneButtonBob-v0', 'VNCOozingForever-v0', 'VNCPacmanPlatform2-v0',
             'VNCPandemonium-v0', 'VNCPapaLouie-v0', 'VNCPixelKnight2-v0',
             'VNCPortalFlash-v0', 'VNCPowerFox4-v0', 'VNCPowerRangers-v0',
             'VNCPrimary-v0', 'VNCRabbitRustler-v0', 'VNCRainbow-v0',
             'VNCRangeman-v0', 'VNCReachForTheSky-v0', 'VNCRevertToGrowth2-v0',
             'VNCRobotAdventure-v0', 'VNCRobotWantsFishy-v0', 'VNCRocket-v0',
             'VNCRocketCar-v0', 'VNCRoverArcher-v0', 'VNCRubbleRacer-v0',
             'VNCRun3-v0', 'VNCSantasDeepFreeze-v0', 'VNCSavingTheCompany-v0',
             'VNCSkyIsland-v0', 'VNCSleepyStusAdventure-v0', 'VNCSnowTrouble-v0',
             'VNCSonicFlash-v0', 'VNCSpaceIsKey-v0', 'VNCSpacemanAce-v0',
             'VNCSuperMarioSunshine64-v0',
             'VNCSuperSmashFlash2-v0', 'VNCSurvivalLab-v0', 'VNCTankWars-v0',
             'VNCTimeForCat-v0', 'VNCTinyCastle-v0', 'VNCTinySquad-v0',
             'VNCUnfinishedShadowGame-v0', 'VNCViridia-v0', 'VNCWeirdville-v0',
             'VNCZombieKnight-v0']:
    register(
        id=game,
        entry_point='gym_vnc.wrappers:WrappedVNCFlashgamesEnv'
    )

register(
    id='VNCNoopFlashgamesEnv-v0',  # Special noop flashgame env
    entry_point='gym_vnc.vnc:WrappedVNCFlashgamesEnv'
)

register(
    id='VNCSuperMario-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCSuperMarioEnv'
)
register(
    id='VNCAsteroidCrash-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCAsteroidCrashEnv'
)

# VNCStarCraft
register(
    id='VNCStarCraft-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCStarCraftEnv',
)

# VNCGTAV
register(
    id='VNCGTAV-v0',
    entry_point='gym_vnc.wrappers:WrappedVNCGTAVEnv',
)
