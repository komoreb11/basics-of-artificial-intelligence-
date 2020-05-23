(define (domain world)
    (:requirements :strips :typing :negative-preconditions)
    (:types hero place item)
    (:predicates
        (at ?where ?what)
        (path ?p1 ?p2)
        (waterpath ?p1 ?p2)
        (own ?i)

        (craftable ?b ?w)
        (craftable_med ?b ?i1 ?i2)
        (craftable_big ?b ?i1 ?i2 ?i3)

        (canswim ?onwhat)
        (canwork ?where)
        (buy ?what ?where)
        (stealable ?what ?where)
        (sell ?what ?where)

        (isalko ?i)
        (iscocaine ?c)
        (grandpa ?p)
        (ismap ?m)
        (isgg ?gg)
        (isgc ?gc)
        (isgi ?gi)
        (isskin ?i)
        (isfrigate ?f)
        (iscaravel ?c)
        (isboat ?b)
        (isflowers ?f)
        (isring ?r)
        
        (alittledrunk)
        (drunk)
        (alkodep)

        (bath ?p)
        (bank ?p)
        (seaplace ?p)
        (bearplace ?p)
        (beerplace ?p)
        (academyplace ?p)
        (pirateplace ?p)
        (pirateproblem ?p)
        (treasureplace ?p)
        (weddingplace ?p)
        (girlhome ?p)
        (smugglerplace ?p)
        (police ?p)

        (Captain)
        (Strong)
        (Smuggler)

        (goodcontacts)
        (badcontacts)
        (criminalrecord)
        (weddingready)

        (HAPPINESS)


    )

    (:action move
        :parameters (?hero - hero ?from - place ?to - place)
        :precondition (and            
            (at ?from ?hero)
            (path ?from ?to)
        )
        :effect (and
            (at ?to ?hero)
            (not (at ?from ?hero))
        )
    )
    (:action swim
        :parameters (?hero - hero ?from - place ?to - place ?i - item)
        :precondition (and            
            (at ?from ?hero)
            (waterpath ?from ?to)
            (not(pirateproblem ?from))
            (own ?i)
            (canswim ?i)
        )
        :effect (and
            (at ?to ?hero)
            (not (at ?from ?hero))
        )
    )
    (:action collect_item
        :parameters (?s - hero ?p - place ?i - item)
        :precondition (and
		      (at ?p ?s)
		      (at ?p ?i )
              (not(pirateproblem ?p))
	    )
        :effect (and 
              (own ?i) 
        ) 
    )
    (:action fightbear
        :parameters (?s - hero ?p - place ?i - item)
        :precondition (and
		      (at ?p ?s)
		      (bearplace ?p)
              (isskin ?i)
	    )
        :effect (and 
              (own ?i)
              (not(bearplace ?p))
              (Strong) 
        ) 
    )
    (:action fight_alittledrunk
        :parameters (?s - hero ?p - place)
        :precondition (and
		      (at ?p ?s)
		      (beerplace ?p)
              (alittledrunk)
	    )
        :effect (and 
              (Strong) 
        ) 
    )
    (:action fight_drunk
        :parameters (?s - hero ?p - place)
        :precondition (and
		      (at ?p ?s)
		      (beerplace ?p)
              (drunk)
	    )
        :effect (and 
              (Strong) 
        ) 
    )
    (:action buy_item
        :parameters (?s - hero ?p - place ?hi - item ?wi - item)
        :precondition (and
		      (at ?p ?s)
		      (buy ?wi ?p )
              (own ?hi)
              (isgg ?hi)
	    )
        :effect (and 
              (own ?wi)
              (not(own ?hi))
        ) 
    )
    (:action sell_item
        :parameters (?s - hero ?p - place ?hi - item ?gc - item)
        :precondition (and
		      (at ?p ?s)
		      (sell ?hi ?p )
              (own ?hi)
              (isgc ?gc)
	    )
        :effect (and 
              (own ?gc)
              (not(own ?hi))
        ) 
    )
    (:action contribution
        :parameters (?s - hero ?p - place ?gg - item ?gc - item)
        :precondition (and
		      (at ?p ?s)
		      (bank ?p)
              (own ?gg)
              (isgg ?gg)
              (isgc ?gc)
	    )
        :effect (and 
              (own ?gc)
              (not(own ?gg))
              (goodcontacts)
        ) 
    )
    (:action invest
        :parameters (?s - hero ?p - place ?gc - item ?gi - item)
        :precondition (and
		      (at ?p ?s)
		      (bank ?p)
              (own ?gc)
              (isgc ?gc)
              (isgi ?gi)
	    )
        :effect (and 
              (own ?gi)
              (not(own ?gc))
              (goodcontacts)
        ) 
    )
    (:action beer_for_all
        :parameters (?s - hero ?p - place ?hi - item ?gc - item)
        :precondition (and
		      (at ?p ?s)
		      (beerplace ?p)
              (own ?gc)
              (isgc ?gc)
	    )
        :effect (and 
              (goodcontacts)
              (not (own ?gc))
        ) 
    )
    (:action craft
        :parameters (?b - item ?w - item )
        :precondition (and
              (own ?w)
              (craftable ?b ?w)
	    )
        :effect (and 
              (own ?b)
              (not(own ?w))
        ) 
    )
    (:action stayalittledrunk
        :parameters (?i - item )
        :precondition(and
            (own ?i)
            (isalko ?i)
            
        )
        :effect (and
            (alittledrunk)
            (not(own ?i))
        )    
    )
    (:action staydrunk
        :parameters (?i - item )
        :precondition(and
            (own ?i)
            (isalko ?i)
            (alittledrunk)
        )
        :effect (and
            (drunk)
            (not(alittledrunk))
            (not(own ?i))
        )    
    )
    (:action staydep
        :parameters (?i - item )
        :precondition(and
            (own ?i)
            (isalko ?i)
            (drunk)
        )
        :effect (and
            (alkodep)
            (not(own ?i))
        )    
    )
    (:action staysober1
        :parameters (?s - hero ?p - place )
        :precondition(and
            (drunk)
            (at ?p ?s)
            (bath ?p)
        )
        :effect (and
            (not(drunk))
            (not(alittledrunk))
        )    
    )
    (:action staysober2
        :parameters (?s - hero ?p - place )
        :precondition(and
            (alittledrunk)
            (at ?p ?s)
            (bath ?p)
        )
        :effect (and
            (not(drunk))
            (not(alittledrunk))
        )    
    )
    (:action craft_big
        :parameters (?b - item ?i1 - item ?i2 - item ?i3 - item)
        :precondition (and
              (own ?i1)
              (own ?i2)
              (own ?i3)
              (craftable_big ?b ?i1 ?i2 ?i3)
	    )
        :effect (and 
              (own ?b)
              (not(own ?i1))
              (not(own ?i2)) 
              (not(own ?i3))
        ) 
    )
    (:action craft_med
        :parameters (?b - item ?i1 - item ?i2 - item)
        :precondition (and
              (own ?i1)
              (own ?i2)
              (craftable_med ?b ?i1 ?i2 )
	    )
        :effect (and 
              (own ?b)
              (not(own ?i1))
              (not(own ?i2)) 
        ) 
    )
    (:action work
        :parameters(?s - hero ?p - place ?i - item)
        :precondition(and
                (canwork ?p)
                (isgg ?i)
                (at ?p ?s)
        )
        :effect (and
            (own ?i)
        )
    )
    (:action stealitem
        :parameters(?s - hero ?p - place ?i - item)
        :precondition(and
                (stealable ?i ?p)
                (at ?p ?s)
        )
        :effect (and
            (own ?i)
            (criminalrecord)
        )
    )
    (:action stay_captain
        :parameters(?s - hero ?p - place ?gc - item)
        :precondition(and
                (academyplace ?p)
                (at ?p ?s)
                (own ?gc)
                (not (criminalrecord))
                (isgc ?gc)
        )
        :effect (and
            (not(own ?gc))
            (Captain)
        )
    )
    (:action pay_bail
        :parameters(?s - hero ?p - place ?i - item)
        :precondition(and
                (at ?p ?s)
                (police ?p)
                (isgg ?i)
                (own ?i)
                (criminalrecord)
        )
        :effect (and
            (not (own ?i))
            (not (criminalrecord))
        )
    )
    (:action erase_criminal_record
        :parameters(?s - hero ?p - place)
        :precondition(and
                (at ?p ?s)
                (police ?p)
                (criminalrecord)
        )
        :effect (and
            (not (drunk))
            (alittledrunk)
            (not (criminalrecord))
        )
    )
    (:action granny
        :parameters(?s - hero ?p - place ?a - item ?m - item)
        :precondition(and
                (grandpa ?p)
                (at ?p ?s)
                (own ?a)
                (isalko ?a)
                (ismap ?m)
        )
        :effect (and
            (own ?m)
            (not (own ?a))
            (badcontacts)
        )
    )
    (:action smugglers
        :parameters(?s - hero ?p - place ?gi - item)
        :precondition(and
                (smugglerplace ?p)
                (at ?p ?s)
                (own ?gi)
                (isgi ?gi)
        )
        :effect (and
            (Smuggler)
        )
    )
    (:action pirate_bad_fight
        :parameters(?s - hero ?p - place ?gc - item ?gg - item ?gi - item ?c - item ?f - item ?b - item)
        :precondition(and
                (at ?p ?s)
                (pirateplace ?p)
                (pirateproblem ?p)
                (not(Strong))
                (isgg ?gg)
                (isgc ?gc)
                (isgi ?gi)
                (isfrigate ?f)
                (iscaravel ?c)
                (isboat ?b)
        )
        :effect (and
            (not (own ?gg))
            (not (own ?gc))
            (not (own ?gi))
            (not (own ?f))
            (not (own ?c))
            (own ?b)
            (Strong)
        )
    )
    (:action pirate_contact
        :parameters(?s - hero ?p - place)
        :precondition(and
                (at ?p ?s)
                (pirateplace ?p)
                (pirateproblem ?p)
                (badcontacts)
        )
        :effect (and
            (alittledrunk)
            (not(drunk))
            (not(pirateproblem ?p))
        )
    )
    (:action pirate_good_fight
        :parameters(?s - hero ?p - place ?gc - item ?gg - item ?gi - item ?c - item ?f - item ?b - item)
        :precondition(and
                (at ?p ?s)
                (pirateplace ?p)
                (Strong)
                (iscaravel ?c)
                (isgg ?gg)
                (isgc ?gc)
                (isgi ?gi)
                (isfrigate ?f)
                (isboat ?b)
                (own ?c)
        )
        :effect (and
            (own ?gg)
            (own ?gc)
            (own ?gi)
            (own ?f)
            (own ?c)
            (own ?b)
            (not(pirateplace ?p))
            (not(pirateproblem ?p))
        )
    )
    (:action woo
        :parameters(?s - hero ?p - place)
        :precondition(and
                (at ?p ?s)
                (girlhome ?p)
                (Strong)
        )
        :effect (and
            (weddingready)
        )
    )
    (:action get_cocaine
        :parameters(?s - hero ?p - place ?m - item ?c - item)
        :precondition(and
                (at ?p ?s)
                (treasureplace ?p)
                (ismap ?m)
                (own ?m)
                (iscocaine ?c)
        )
        :effect (and
            (own ?c)
        )
    )
    (:action wedding
        :parameters(?s - hero ?p - place ?r - item ?f - item)
        :precondition(and
                (at ?p ?s)
                (weddingready)
                (weddingplace ?p)
                (not(criminalrecord))
                (own ?r)
                (isring ?r)
                (own ?f)
                (isflowers ?f)
                (goodcontacts)
                (not (alittledrunk))
                (not(drunk))
                (not(alkodep))
        )
        :effect (and
            (HAPPINESS)
        )
    )
    (:action stay_admiral
        :parameters(?s - hero ?p - place ?a - place)
        :precondition(and
                (at ?a ?s)
                (academyplace ?a)
                (seaplace ?p)
                (not(pirateplace ?p))
                (Captain)
                (not (alittledrunk))
                (not(drunk))
                (not(alkodep))
        )
        :effect (and
            (HAPPINESS)
        )
    )
    (:action rocknroll
        :parameters(?c - item ?f - item ?gi - item)
        :precondition(and
                (own ?c)
                (iscocaine ?c)
                (isfrigate ?f)
                (own ?f)
                (isgi ?gi)
                (own ?gi)
                (alkodep)
                (Smuggler)
        )
        :effect (and
            (HAPPINESS)
        )
    )


)


