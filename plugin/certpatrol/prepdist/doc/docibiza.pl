package prep;


# called by #head
#
sub do_head { my ($short,$long) = @_; print <<X; }

<body bgcolor="#339966" link="#ff3333" vlink="#cc0066">
<center><table cellpadding=9 bgcolor="#33cc99" width=444><tr><td align=right>

<font size=9>$short</font><br>
<font size=4>$long</font><p>

</td></tr><tr><td>
X


# used somewhere
#
sub do_button { my ($text) = @_; print <<X; }
<b><font size=2>$text</font></b>
X


# a demonstration of the power of prep. see prep.xht
#
sub do_box { my ($url, $title) = @_; print <<X; }
<div align=center><table bgcolor=black cellspacing=0 border=0><tr><th>
<table bgcolor=white cellspacing=0 border=0><tr><th>
<table bgcolor="#ffcc66" cellpadding=3 cellspacing=0 border=0><tr><td>
<a href="$url"><img src=internal-gopher-menu border=0></a>
$title
</td></tr></table>
</th></tr></table>
</th></tr></table></div>
X


# called automatically at end of document
#
sub done { print <<X; }

</td></tr></table></center>
X


# make require happy

1;
