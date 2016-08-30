import gym
from gym.scoreboard import add_task, add_group
from gym_vnc.scoreboard.benchmark import registry, add_benchmark, add_task_to_benchmark

# Benchmarks

add_benchmark(
    id='Games-v0',
    name='Games benchmark',
    description='The benchmark allows `supervised pre-training <http://10.6.103.167:41234/>`_ in 950 demonstration environments. Agents must learn the benchmark environments without demonstration.'
)

atari = gym.scoreboard.registry.groups['atari']

for env_id in atari['envs']:
    if '-ram-' not in env_id:
        add_task_to_benchmark('Games-v0', env_id)

# Scoreboard groups

add_group(
    id='vnc_flashgames',
    name='VNC Flashgames',
    description='Browser Flash games served through VNC',
)

# Scoreboard tasks

for game in ['VNC42Game-v0', 'VNCAirBattle-v0', 'VNCAmberialAxis-v0',
             'VNCAsteroidCrash-v0', 'VNCAthletics-v0', 'VNCAvalancher-v0',
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
             'VNCSuperMario-v0', 'VNCSuperMarioSunshine64-v0',
             'VNCSuperSmashFlash2-v0', 'VNCSurvivalLab-v0', 'VNCTankWars-v0',
             'VNCTimeForCat-v0', 'VNCTinyCastle-v0', 'VNCTinySquad-v0',
             'VNCUnfinishedShadowGame-v0', 'VNCViridia-v0', 'VNCWeirdville-v0',
             'VNCZombieKnight-v0']:
    add_task(
        id=game,
        group='vnc_flashgames',
    )
