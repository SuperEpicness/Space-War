# -*- mode: python -*-

block_cipher = None

path = 'C:\\Users\\Simon\\Documents\\Washington_FWHS\\CG&SP_SimonS_FWHS'
a = Analysis(['main.py'],
             pathex=[path],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

data_files = []
files = ['Alerts\\alert1_left.png', 'Alerts\\alert1_right.png', 'Alerts\\alert2_left.png', 'Alerts\\alert2_right.png', 'Alerts\\alert3_left.png', 'Alerts\\alert3_right.png', 'Asteroids\\asteroid1.png', 'Asteroids\\asteroid2.png', 'Asteroids\\asteroid3.png', 'Asteroids\\sm1_asteroid1.png', 'Asteroids\\sm1_asteroid2.png', 'Asteroids\\sm1_asteroid3.png', 'Asteroids\\sm2_asteroid1.png', 'Asteroids\\sm2_asteroid2.png', 'Asteroids\\sm2_asteroid3.png', 'Asteroids\\sm3_asteroid1.png', 'Asteroids\\sm3_asteroid2.png', 'Asteroids\\sm3_asteroid3.png', 'Asteroids\\xs1_asteroid1.png', 'Asteroids\\xs1_asteroid2.png', 'Asteroids\\xs2_asteroid1.png', 'Asteroids\\xs2_asteroid2.png', 'Asteroids\\xs3_asteroid1.png', 'Asteroids\\xs3_asteroid2.png', 'Instructions\\instructions.png', 'Planets\\Planet01.png', 'Planets\\Planet02.png', 'Planets\\Planet03.png', 'Planets\\Star01.png', 'Powerups\\blank.png', 'Powerups\\healthup.png', 'Powerups\\lifeup.png', 'Powerups\\rapidfire.png', 'Sounds\\Explosion1.wav', 'Sounds\\Explosion2.wav', 'Sounds\\Explosion3.wav', 'Sounds\\Explosion4.wav', 'Sounds\\Hit.wav', 'Sounds\\LaserSFX.wav', 'Sounds\\Powerup1.wav', 'Sounds\\Powerup2.wav', 'Sounds\\Powerup3.wav', 'ArcadeFont.TTF', 'bomb.png', 'bomber_l.png', 'bomber_r.png', 'bullet.png', 'crosshairs.png', 'enemy01.png', 'explode.png', 'explosion1.png', 'gun.png', 'highscores.txt', 'icon.png', 'laser1.png', 'laser2.png', 'logo.png', 'missile_off.png', 'missile1.png', 'missile2.png', 'player.png', 'shiptexture.png']

for f in files:
    data_files.append((f, path + '\\RESOURCES\\' + f, 'DATA'))

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas + data_files,
          name='mothership',
          debug=False,
          strip=False,
          upx=True,
          console=True )
