from en_gb import G2P

g2p = G2P()
print(g2p.convert('hello'))
print(g2p.convert('github'))

from en_us import G2P

g2p = G2P()
print(g2p.convert('hello'))
print(g2p.convert('github'))

from zh_cn import G2P

g2p = G2P()
print(g2p.convert('今天天气不错'))
print(g2p.convert('好吧', False))
