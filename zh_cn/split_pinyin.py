#!/bin/python3
# Tranlated from the perl version

def split_pinyin(pinyin):
    initial = ''

    # retrieve tone
    if pinyin[-1] >= '0' and pinyin[-1] <= '9':
        tone = int(pinyin[-1])
        if tone == 0:
            tone = 5
        pinyin = pinyin[:-1]
    else:
        tone = 5

    # check Erhua (retroflex): Pinyin is not "er" and ending with "r"
    erhua = ''
    if pinyin != 'er' and pinyin[-1] == 'r':
        pinyin = pinyin[:-1]
        erhua = 'rr'

    # get initial, final
    if pinyin[0] == 'y':
        # ya->ia, yan->ian, yang->iang, yao->iao, ye->ie, yo->io, yong->iong, you->iou
        # yi->i, yin->in, ying->ing
        # yu->v, yuan->van, yue->ve, yun->vn
        pinyin = 'i' + pinyin[1:]
        if pinyin[1] == 'i':
            pinyin = pinyin[1:]
        elif pinyin[1] in 'uv':
            pinyin = 'v' + pinyin[2:]
        final = pinyin
    elif pinyin[0] == 'w':
        # wa->ua, wo->uo, wai->uai, wei->uei, wan->uan, wen->uen, wang->uang, weng->ueng
        # wu->u
        # change 'w' to 'u', except 'wu->u'
        pinyin = 'u' + pinyin[1:]
        if pinyin[1] == 'u':
            pinyin = pinyin[1:]
        final = pinyin
    elif pinyin in ['ng', 'm', 'n']:
        # ng->ng, n->n, m->m
        final = pinyin
    else:
        # get initial and final
        # initial should be: b p m f d t n l g k h j q x z c s r zh ch sh
        final = pinyin
        if len(pinyin) > 1 and pinyin[:2] in ['ch', 'sh', 'zh']:
            initial = pinyin[:2]
            final = pinyin[2:]
        elif pinyin[0] in 'bpmfdtnlgkhjqxzcsr':
            initial = pinyin[:1]
            final = pinyin[1:]

        # the final of "zi, ci, si" should be "ix"
        if initial in ['c', 's', 'z'] and final == 'i':
            final = 'ix'
        # the final of "zhi, chi, shi, ri" should be "iy"
        elif initial in ['ch', 'r', 'sh', 'zh'] and final == 'i':
            final = 'iy'
        # ju->jv, jue->jve, juan->jvan, jun->jvn,
        # qu->qv, que->qve, quan->qvan, qun->qvn,
        # xu->xv, xue->xve, xuan->xvan, xun->xvn
        # change all 'u' to 'v'
        elif initial in ['j', 'q', 'x']:
            final = final.replace('u', 'v')
        # ui->uei
        # iu->iou
        # un->uen
        if final == 'ui':
            final = 'uei'
        elif final == 'iu':
            final = 'iou'
        elif final == 'un':
            final = 'uen'

    return (initial, final, tone, erhua)

if __name__ == '__main__':
    import sys
    print(split_pinyin(sys.argv[1]))
