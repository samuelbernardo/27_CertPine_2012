sub langtabs {
	my $color = shift;
	$color = '#000000' unless $color;
	my $fn = shift;
	$fn = 'index' unless $fn;
	my $lang = shift;
	# $lang = 'en' unless $lang;

	print <<X;
<table border=0 cellspacing=0 cellpadding=5><tr bgcolor="$color">
<td><font size=1>&#160;»
X
	my %l = (
		it => 'ITALIANO',
		fr => 'FRANÇAIS',
		es => 'ESPAÑOL',
		en => 'ENGLISH',
		de => 'DEUTSCH',
	);
	foreach $l (reverse sort keys %l) {
		if ($l eq $lang) {
			print <<X;
$l{$l} »
X
			next;
		}
		my $file = "$fn.$l.html";
		print <<X if -r "$'PHYSICAL$file";
<a href="$file">$l{$l}</a> »
X
	}
	print <<X;
</font></td></tr></table>
X
}

1;
