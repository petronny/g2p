sub split_pinyin($)
{
	# split Pinyin into initial, final, tone, and erhua_flag
	my ($pinyin) = @_;
	my $initial = "";
	my $final = "";
	my $erhua = "";
	my $tone = 5;
	
	# retrieve tone
	$pinyin =~ s/([0-9]?)$//;
	$tone = $1;
	$tone =~ s/^$/5/; # neutral tone if no tone found
	
	# check Erhua (retroflex): Pinyin is not "er" and ending with "r"
	$erhua = "";
	if ($pinyin ne "er" && $pinyin =~ /^(.+)(r)$/)
	{
		$pinyin = $1; # remove ending "r"
		$erhua = "rr";
	}
	
	# get initial, final
	if ($pinyin =~ /^y/)
	{
		# ya->ia, yan->ian, yang->iang, yao->iao, ye->ie, yo->io, yong->iong, you->iou
		# yi->i, yin->in, ying->ing
		# yu->v, yuan->van, yue->ve, yun->vn
		$pinyin =~ s/^y/i/;
		$pinyin =~ s/^ii/i/;
		$pinyin =~ s/^iu/v/;
		$pinyin =~ s/^iv/v/;
		$final = $pinyin;
		$initial = "";
	}
	elsif ($pinyin =~ /^w/)
	{
		# wa->ua, wo->uo, wai->uai, wei->uei, wan->uan, wen->uen, wang->uang, weng->ueng
		# wu->u
		# change 'w' to 'u', except 'wu->u'
		$pinyin =~ s/^w/u/;
		$pinyin =~ s/^uu/u/;
		$final = $pinyin;
		$initial = "";
	}
	elsif ($pinyin =~ /^ng$|^n$|^m$/)
	{
		# ng->ng, n->n, m->m
		$final = $pinyin;
		$initial = "";
	}
	else
	{
		# get initial and final
		# initial should be: b p m f d t n l g k h j q x z c s r zh ch sh
		$initial = "";
		$final = $pinyin;
		if ($pinyin =~ /^(zh|ch|sh|[bpmfdtnlgkhjqxzcsr])(.+)$/)
		{
			$initial = $1;
			$final = $2;
		}
		
		# the final of "zi, ci, si" should be "ix"
		$final = "ix" if ($final =~ /^i$/ && $initial =~ /^(z|c|s)$/);
		
		# the final of "zhi, chi, shi, ri" should be "iy"
		$final = "iy" if ($final =~ /^i$/ && $initial =~ /^(zh|ch|sh|r)$/);
		
		# ju->jv, jue->jve, juan->jvan, jun->jvn,
		# qu->qv, que->qve, quan->qvan, qun->qvn,
		# xu->xv, xue->xve, xuan->xvan, xun->xvn
		# change all 'u' to 'v'
		$final =~ s/^u/v/ if ($initial =~ /^(j|q|x)$/);
		
		# when there is initial
		# ui->uei
		# iu->iou
		# un->uen
		$final =~ s/^ui$/uei/;
		$final =~ s/^iu$/iou/;
		$final =~ s/^un$/uen/;
	}
	
	print "$initial\t$final\t$tone\t$erhua\n";
	return ($initial, $final, $tone, $erhua);
}
