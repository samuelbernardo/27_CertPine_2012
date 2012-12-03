#getdnsbyip.pl
#read ip addresses from a text file and send them to a search engine
#supporting ip search, then index all found domains and subdomains
# Author:  DiabloHorn (KD-Team)
# Greetz: pointdxtr
# Date: 06-04-2008
# Version: 0.2

#changes
# fixed url traversing bug
# fixed the - bug

use LWP::UserAgent;
use HTML::LinkExtor;
use URI::URL;

#######CHANGE ON OWN RISK#######
my $baseSEngine = "http://search.live.com";
#######END OF CHANGE SECTION####
$numArgs = $#ARGV + 1;

if($numArgs != 1){
	print "getdnsbyip.pl <file with ips>\n";
	print "Example: getdnsbyip.pl input.txt\n";
	print "Should find all (sub)domains hosted on the ip(s)";
	exit(1);
}

$filename = $ARGV[0];

open(IPFILE, $filename) or die("File $filename could not be opened!");
@all_ip = <IPFILE>;
close(IPFILE);

#setup some things
#start url for searching
$ua = LWP::UserAgent->new;
$ua->agent('Opera/9.20 (Windows NT 6.0; U; en)'); #this should help us a little to fool google.
$p = HTML::LinkExtor->new(\&callback);
#hash containing all found sub domains
%allurls = ();
#hash containing all the "next" urls from google
%nexturls = {};
#end of things setup

foreach $line (@all_ip)
{
	chomp($line);
	print "[*] Searching (sub)domains on $line\n";
	getdomains($line);
	undef(%allurls);
	undef(%nexturls);
	#my $rndTime = getRandomInt(7,60);
	#print "[*] Sleeping for $rndTime seconds\n";
	#sleep $rndTime;
	#undef($rndTime);
}

sub callback {
 my($tag, %attr) = @_;
 #for this poc we are only interested in the <a href> tags
 return if $tag ne 'a';
 my @links = values %attr;
 foreach $link(@links){
	#extract all urls that contain the base domain
	if($link =~ m!(^(http://|https://|ftp://|irc://)(([a-zA-Z0-9\-\.]*)(\.+))*[a-zA-Z0-9\-\.]*)!io){
		if(!($link =~ m!.(live\.com|microsoft\.com|msnscache\.com|WindowsLiveTranslator\.com|msn\.com)!io)){
			if (!exists $allurls{$1}){
				$allurls{$1} = $1;
				print "$1\n";
			}
		}
	}

	#extract the next urls
	if($link =~ m!^/results\.aspx\?q=.*!io){
		if (!exists $nexturls{$link}){
			$nexturls{$link} = $link;
		}
	}
 }
 
}

sub getdomains{
	my $ip = $_[0];
	my $url = URI->new("$baseSEngine/results.aspx?q=ip%3A$ip");
	my $res = $ua->request(HTTP::Request->new(GET => $url),sub {$p->parse($_[0])});
	my $visitedGURLS = 0;
	
	while(1){
		if($visitedGURLS == scalar keys(%nexturls)){
			last;
		}

		foreach $nurl(sort keys(%nexturls)){
			my $value = $nexturls{$nurl};
			#prevent parsing pages twice
			if($value ne "visited"){
				my $temp = URI->new($baseSEngine.$value);
				#you can comment this out if you only want clean finds.
				#print "[*] searching next page $temp\n";
				$res = $ua->request(HTTP::Request->new(GET => $temp),sub {$p->parse($_[0])});
				$nexturls{$nurl} = "visited";
				$visitedGURLS++;
				sleep 3; #try and prevent getting blocked by google
			}
		}	
	}
	undef($url);
	undef($res);
	undef($visitedGURLS);	
}

#calculate random number between value1 and value2
#ex: getRandomInt(5,10);
#it overflows the second,I'm lazy
sub getRandomInt{
	my $min = $_[0];
	my $range = $_[1];
	srand(time());
	return $random_number = int(rand($range)+$min);
}

