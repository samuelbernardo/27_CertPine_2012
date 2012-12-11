# $Id: prep.pl,v 1.8 2007/07/03 13:20:14 lynx Exp $
#
### PREP: the PRE Processor.
# -	simple and nifty
#	i thought a preprocessor shouldn't take more than 500 lines of perl,
#	that's why it takes about 200 lines.
# -	handy for managing html document trees
# -	the alternative choice when you've had enough of SGML
#
## Copyright since 1994 by Carlo von Loesch.
##			(psyc://psyced.org/~lynX)
## All rights reserved.
#
# allows flags to be passed as args
# knows (((command args))) inline replacements
# knows hierarchical #if/#else/#endif constructs
# knows #define, #include and #ifn. new: #set
# knows #require to extend the # command set (#doctype is also accepted)
# removes # comments
# knows X) flag prefixes
# knows XY) combined flag prefixes
# knows "#pragma or" to apply OR instead of AND with combined-flag-prefixes
# knows '#pragma keephash' to allow lines with leading hash sign
#
# dont be surprised, this code happens to still be perl4 compliant

package prep;

$block = 0;
$level = 0;

$keephash = 0;

## PUBLIC FUNCTIONS

sub run {
	$FILE_NAME = shift;
	$FLAGS = shift;
	my $rawdata = shift;
	%VAR = @_;

	&init($FLAGS) if $FLAGS;
	&define('E') if $FILE_NAME =~ /\.(en)\./i;
	&define('D') if $FILE_NAME =~ /\.(de)\./i;
	&define('F') if $FILE_NAME =~ /\.(fr)\./i;
	&define('I') if $FILE_NAME =~ /\.(it)\./i;
	&define('S') if $FILE_NAME =~ /\.(es)\./i;
#	$LANGUAGE = $1;	# only defined if given by argument
	$LANGUAGE = 'en' if &flag('E');
	$LANGUAGE = 'de' if &flag('D');
	$LANGUAGE = 'fr' if &flag('F');
	$LANGUAGE = 'it' if &flag('I');
	$LANGUAGE = 'es' if &flag('S');

	# other popular flags:
	#	N - netscape only
	#	X - exploder only
	#	P - print edition

	&doing if defined &doing;
	if ($rawdata) {
		foreach(split(/\n/, $rawdata)) {
			&prep($_);
		}
	} else {
		&include($FILE_NAME);
	}
	&done if defined &done;
}

## END OF PUBLIC FUNCTIONS

sub init {
	local($a) = @_;
	undef %FLAGS;
	$FLAGS = $a;
	$FLAGS =~ s/-//go;
	$OR = &flag('|') ? 1 : 0;	# flag for and/or logic, default is and
}

sub prep {
	local($_) = @_;
	study;
	s/\r?\n?$//;		# remove line delimiters

	if (/(.*)\\$/o) {	# support for \ line merging
		$nl = '';
		$_ = $1;
	} else {
		$nl = "\n";
	}

	($pre, $post) = /^([A-Z]+)\)(.*)/o;	# support for flag) syntax
	if ($pre) {
		local($state) = 0;
		foreach(split('', $pre)) {
			$FLAGS{$pre}++;
			if ($OR ^ (index($FLAGS, $_) < 0)) {
				$state = 1; last;
			}
		}
		return if $state ^ $OR;
		$_ = $post;
	}

	# support for leading #
	if (/^#/) {
		return if /^##/;	# psyced style comments

		# else/endif need to be checked before ifdef
		&else($1), return if /^#else\b(.*)/o;
		&endif($2), return if /^#(endif|fi)\b(.*)/o;

		&ifdef($2), return if /^#i(f|fdef)\s+(\S+)\s*$/o;
		&ifndef($2), return if /^#if(n|ndef)\s+(\S+)\s*$/o;

		unless ($block) {
		    &define($2), return if /^#de(f|fine)\s+(\S+)\s*$/o;
		    &include($2), return if /^#in(c|clude)\s+(\S+)\s*$/o;
		    &require($2), return if /^#(require|doctype)\s+(\S+)\s*$/o;
		    &set($1,$2), return if /^#set\s+(\S+)\s+(.+)\s*$/o;
		    &pragma($1), return if /^#pragma\s+(\S+)\s*$/o;
		    if ( not $keephash and /^#(\w+)\s*(.*?)\s*$/ ) {
			my $i = &interpret($1, $2);
			print $i if $i and length($i) > 2;	# careful conversion
		    }
		}
		return unless $keephash;
	}

	unless ($block) {
		$_ = &text($_) if $CATCH_TEXT;

		# support for inline ((( )))
		# muve.pl needs this to happen *after* catch-text
		s/\(\(\(\s*(\w+)\s*(.*?)\s*\)\)\)/&interpret($1, $2)/ge;

		print $_, $nl;
	}
}


sub flag {
	local($x) = @_;
	return index($FLAGS, $x) >= 0;
}
sub expr {
	local($_) = @_;
	local($true);

	if (/^(1|0)$/) {
		$true = $1;
	} elsif (/^!\s*(\w+)$/) {
		$true = ! &flag($1);
	} elsif (/^(\w+)$/) {
		$true = &flag($1);
	} else {
		eval '$true='. $_ .';';
	}

	return $true;
}


sub ifdef {
	local($x) = @_;
	$FLAGS{$x}++;

	$level++;
        unless ($block) {
		$block = $level unless &expr($x);
        }
        print "- $x ? - level $level - block $block -\n\n" if $DEBUG;       
}
sub ifndef {
	local($x) = @_;
	$FLAGS{$x}++;

	$level++;
        unless ($block) {
		$block = $level if &expr($x);
        }
        print "- $x ? - level $level - block $block -\n\n" if $DEBUG;       
}
sub else {
	$block=$level,return unless $block;
	$block=0 if $level == $block;
	print "- else - level $level - block $block -\n\n" if $DEBUG;
}
sub endif {
	$block=0 if $level == $block;
	--$level;
	die 'endif without if' if $level < 0;
	print "- endif - level $level - block $block -\n\n" if $DEBUG;
}
sub define {
	local($_) = @_;
	$FLAGS .= $_;
}


sub set {
	my $v = shift;
	my $val = shift;
# i can't remember why i coded it this way and
# i can't find a single app that uses this, so
# i'll change it the way i need it for my wiki prep
#	${$v} = $val;
	$VAR{$v} = $val;
}
sub pragma {
	local($_) = @_;
	$OR = 0 if /\bAND\b/io;
	$OR = 1 if /\bOR\b/io;
	$keephash = 1 if /\bKEEPHASH\b/io;
}
sub require {
	local($x) = @_;
	$x .= '.pl';
	$t = './'.$x;
	require $t, return if -r $t;
	# $t = $HOME.'/'.$x.'.pl';
	# require $t, return if -r $t;
	# $t = $LIB.'/'.$x.'.pl';
	require $x;
}
sub include {
	local($x) = @_;
	local(*I);

	open(I, "$'PHYSICAL$x") or
	  open(I, $x) or die "unable to #include $x (current dir: ". `pwd` .')';
	while (<I>) { &prep($_); }
	close I;
}
sub interpret {
	local($cmd, $args) = @_;
#print STDERR "[[[ $cmd: $VAR{$cmd} ]]]\n";
	return $VAR{$cmd} if $VAR{$cmd} &&! $args;

	my $func = "do_$cmd";
	return unless defined &$func;
	my $ret;

	@A = split(/\s+\,\s+/, $args);
	$@ = undef;
	eval "\$ret = &$func(\@A)";
	if ($@) {
		die "\n#$cmd $args:\n", $@, "\n";
	}
	return $ret;
}

1;
