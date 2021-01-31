command = """
@commands.command()
async def command{version}(self, ctx):
    print('command {version}')
"""

for cmd in range(30):
    cmd = "{:02d}".format(cmd)
    print(command.format(version=cmd))