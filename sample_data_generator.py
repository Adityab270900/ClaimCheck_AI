import random
from datetime import datetime, timedelta

def generate_sample_data():
    """
    Generate sample data for claims and myth articles.
    
    Returns:
        tuple: (claims_data, myths_data)
    """
    # Generate claims data
    claims_data = generate_claims_data()
    
    # Generate myths data
    myths_data = generate_myths_data()
    
    return claims_data, myths_data

def generate_claims_data():
    """
    Generate sample claims data.
    
    Returns:
        list: List of dictionaries with sample claims
    """
    claims = [
        {
            'claim_id': 1,
            'claim_text': "I saw a ghost that walked through walls last night at the old mansion.",
            'claim_date': '2023-01-15',
            'domain': 'Ghost Myths'
        },
        {
            'claim_id': 2,
            'claim_text': "UFOs were spotted over the city last week with flashing lights that no airplane could make.",
            'claim_date': '2023-02-03',
            'domain': 'UFO Encounters'
        },
        {
            'claim_id': 3,
            'claim_text': "When Mercury is in retrograde, electronic devices malfunction more frequently.",
            'claim_date': '2023-03-21',
            'domain': 'Astrology'
        },
        {
            'claim_id': 4,
            'claim_text': "I can bend spoons with my mind through telekinesis.",
            'claim_date': '2023-04-10',
            'domain': 'Supernatural Powers'
        },
        {
            'claim_id': 5,
            'claim_text': "The Bermuda Triangle causes ships and planes to mysteriously disappear.",
            'claim_date': '2023-05-05',
            'domain': 'Supernatural Powers'
        },
        {
            'claim_id': 6,
            'claim_text': "Are goat sacrifices sacred and do they have supernatural powers?",
            'claim_date': '2023-06-18',
            'domain': 'Supernatural Powers'
        }
    ]
    
    return claims

def generate_myths_data():
    """
    Generate sample myths data.
    
    Returns:
        list: List of dictionaries with sample myths
    """
    # Ghost myths
    ghost_myths = [
        {
            'source_id': 'GM001',
            'source': 'Journal of Paranormal Investigations',
            'publication_date': '2022-07-15',
            'domain': 'Ghost Myths',
            'text': """
            Ghost sightings are among the most common paranormal claims, but they can often be explained by natural phenomena. 
            When people report seeing figures that walk through walls, this is typically attributed to one of several causes: 
            pareidolia (the tendency to see patterns in random stimuli), sleep paralysis, or hypnagogic hallucinations that occur 
            between wakefulness and sleep. Studies have shown that when people are in old or unfamiliar buildings, especially those 
            with cultural associations to hauntings, they are more likely to interpret normal sensory experiences as paranormal. 
            Additionally, infrasound (low-frequency sound that humans can't consciously hear) can cause feelings of unease, anxiety, 
            and even visual hallucinations - and old buildings often have structural properties that generate infrasound. 
            Scientific investigations of claimed ghost sightings consistently find natural explanations when rigorous methods are applied.
            Many ghost sightings occur in low light conditions where the human visual system is particularly prone to errors and 
            misinterpretations. The "walking through walls" phenomenon specifically is most commonly reported when witnesses are in a state 
            of high suggestibility or during periods of wakefulness surrounded by sleep, when the brain can project dream-like images onto 
            the real environment. No ghost sighting has ever been scientifically verified under controlled conditions.
            """
        },
        {
            'source_id': 'GM002',
            'source': 'Scientific American: Psychology of Belief',
            'publication_date': '2023-01-20',
            'domain': 'Ghost Myths',
            'text': """
            The persistent belief in ghosts despite lack of scientific evidence represents an interesting case study in human psychology. 
            When examining reports of ghost sightings in old mansions and historic buildings, researchers have identified several contributing factors. 
            First, confirmation bias leads people who already believe in ghosts to interpret ambiguous stimuli as paranormal. Second, the power of suggestion 
            is extremely strong - people who are told a location is haunted report more unusual experiences than control groups. Third, environmental factors 
            in old buildings such as drafty air currents, settling foundations causing creaking sounds, and unusual electromagnetic fields can create sensory 
            experiences that seem supernatural. Fourth, sleep disruptions in unfamiliar environments can trigger hypnagogic or hypnopompic hallucinations that 
            seem incredibly real. The appearance of figures "walking through walls" specifically can be explained by misperceptions during brief micro-sleeps or 
            the brain filling in missing visual information. Additionally, cultural narratives about haunted locations prime people to interpret their experiences 
            within that framework. Psychological experiments have demonstrated that even skeptical individuals can be susceptible to interpreting normal stimuli 
            as paranormal when placed in the right suggestive environment.
            """
        }
    ]
    
    # UFO myths
    ufo_myths = [
        {
            'source_id': 'UFO001',
            'source': 'Journal of Atmospheric Physics',
            'publication_date': '2022-09-08',
            'domain': 'UFO Encounters',
            'text': """
            Unidentified Flying Objects (UFOs) are frequently reported as displaying lighting patterns and movements unlike conventional aircraft. 
            However, scientific analysis of UFO reports reveals common misidentifications. Atmospheric phenomena such as ball lightning, St. Elmo's fire, 
            and light refraction through temperature inversions can create the appearance of strange lights in the sky. Modern technology also contributes: 
            LED lights on drones can be programmed to display patterns and colors that appear extraordinary, especially when viewed from a distance without 
            reference points. Satellites, especially Starlink satellite trains, have been responsible for numerous recent UFO reports. The human visual 
            system is particularly poor at judging the distance, size, and speed of lights in the night sky, leading to misperceptions of ordinary aircraft, 
            planets, or stars as performing "impossible" maneuvers. High-altitude military aircraft tests have historically been responsible for many UFO waves. 
            When viewed obliquely, conventional aircraft lights can appear to move in ways that seem to defy physics to ground observers. Multiple studies of 
            UFO reports have found that over 95% can be explained by known phenomena when sufficient information is available. The remaining cases typically 
            suffer from insufficient data rather than requiring extraordinary explanations.
            """
        },
        {
            'source_id': 'UFO002',
            'source': 'Aerospace Technology Review',
            'publication_date': '2023-03-12',
            'domain': 'UFO Encounters',
            'text': """
            Reports of unusual light patterns associated with alleged UFO sightings have been extensively studied by aviation and atmospheric scientists. 
            Modern aircraft, both commercial and military, employ increasingly complex lighting systems that can appear highly unusual to observers unfamiliar 
            with aviation standards. Military aircraft in particular often test new lighting configurations that may not match civilian expectations. 
            Weather phenomena create additional complexity - ice crystals in high atmosphere can refract and reflect aircraft lights in ways that make single 
            light sources appear as multiple moving objects. Plasma phenomena in the upper atmosphere, while rare, can generate luminous displays that defy 
            conventional explanation for observers. Digital photography artifacts further complicate identification - lens flares, long exposures, and digital 
            processing can all create apparent anomalies that don't represent physical objects. Meteorological research balloons carrying instrument packages 
            with LED indicators have been confirmed as the source of multiple "flashing UFO" reports. The perception that certain light movements represent 
            "impossible physics" typically results from observer misperception of distance and three-dimensional movement rather than actual violations of 
            physical laws. When triangulation and multiple instrument recordings are possible, these apparently anomalous movements resolve into conventional 
            phenomena following normal physical principles.
            """
        }
    ]
    
    # Astrology myths
    astrology_myths = [
        {
            'source_id': 'AS001',
            'source': 'Journal of Statistical Analysis',
            'publication_date': '2022-08-19',
            'domain': 'Astrology',
            'text': """
            The claim that Mercury retrograde periods correlate with increased electronic malfunctions has been scientifically examined in multiple studies. 
            Mercury retrograde refers to an optical illusion where Mercury appears to move backward in its orbit relative to Earth. Astrological traditions 
            suggest this period influences communication, technology, and travel disruptions. However, statistical analyses of electronic device failure rates, 
            IT system outages, and technology service calls show no correlation with Mercury retrograde periods. A comprehensive study examining 10 years of 
            technology repair data across multiple companies found equivalent failure rates during retrograde and non-retrograde periods when controlling for 
            other variables. Electronic devices function based on established electromagnetic and quantum principles that cannot be influenced by the apparent 
            position of planets several million miles away. The gravitational effect of Mercury on Earth's technology is infinitesimal compared to local 
            influences. Additionally, controlled studies of participant-reported technology issues during blind conditions (where participants didn't know 
            whether Mercury was retrograde) showed that only participants who were told Mercury was retrograde reported higher technology issues, demonstrating 
            a clear confirmation bias effect. The persistence of this belief represents a combination of confirmation bias, pattern recognition errors, and 
            the tendency to seek meaning in coincidental events.
            """
        },
        {
            'source_id': 'AS002',
            'source': 'Cognitive Science Quarterly',
            'publication_date': '2023-02-05',
            'domain': 'Astrology',
            'text': """
            Belief in astrological phenomena such as Mercury retrograde effects on technology represents a fascinating case study in cognitive biases. 
            When people believe Mercury retrograde affects electronic devices, they become hyperaware of technical problems during these periods while 
            giving less attention to identical problems during other times. This selective attention creates an illusion of correlation where none exists. 
            Electronic malfunctions occur randomly throughout the year based on normal failure rates of components, software bugs, network issues, and 
            user error. Data centers and technology companies report no statistically significant increase in incident rates during retrograde periods. 
            The vast distances in our solar system make any causal mechanism physically impossible - Mercury's gravitational influence on Earth is 
            approximately 0.000000000667 times that of standard gravity and is further dwarfed by the gravitational influences of other nearby objects. 
            Moreover, retrograde motion itself is merely an optical illusion from our viewing perspective, not an actual reversal of a planet's orbit. 
            Experimental psychology has demonstrated that when people are primed to expect technology problems (by being told Mercury is retrograde), 
            they report more issues and frustration with identical systems compared to control groups, highlighting how expectation shapes experience. 
            The persistence of Mercury retrograde beliefs illustrates how pre-scientific explanatory frameworks continue to influence perception in 
            the modern technological age.
            """
        }
    ]
    
    # Supernatural powers myths
    supernatural_myths = [
        {
            'source_id': 'SP001',
            'source': 'Journal of Paranormal Investigation',
            'publication_date': '2022-11-30',
            'domain': 'Supernatural Powers',
            'text': """
            Claims of telekinesis - the ability to move objects with the mind - have been extensively tested under controlled scientific conditions. 
            Despite thousands of experimental trials over several decades, no reproducible evidence for telekinesis has ever been established. 
            The most famous claims, including spoon bending demonstrations popularized by Uri Geller in the 1970s, have been thoroughly debunked 
            as sleight of hand tricks. Professional magicians can easily replicate all claimed telekinetic feats using standard magic techniques. 
            Controlled experiments by parapsychologists initially reported small statistical effects, but these disappeared when more rigorous 
            controls were implemented to prevent unconscious movement, sensory leakage, and experimenter bias. Modern telekinesis experiments using 
            sensitive detection equipment can measure movements at the quantum level, yet still fail to find any evidence that human intention can 
            affect physical objects without touch. Brain imaging studies show no unusual energy emissions or unknown mechanisms that could enable 
            such effects. The persistence of telekinesis claims typically involves some combination of ideomotor effects (unconscious muscle movements), 
            magic techniques, and perceptual biases among observers. Scientific consensus across physics, neuroscience, and psychology concludes that 
            telekinesis contradicts established physical laws governing energy and force, and lacks any empirical support despite extensive testing.
            """
        },
        {
            'source_id': 'SP002',
            'source': 'Skeptical Inquirer',
            'publication_date': '2023-01-15',
            'domain': 'Supernatural Powers',
            'text': """
            The history of spoon bending claims provides an instructive case study in the investigation of paranormal claims. While numerous individuals 
            have claimed the ability to bend metal objects using only mental powers, these claims have consistently failed under properly controlled 
            conditions. Professional magicians and mentalists regularly perform spoon bending as part of their acts, using techniques that include 
            pre-stressed metal, misdirection, and clever handling. When famous "psychic" spoon benders have been prevented from touching the spoons 
            before the demonstration, having their hands blocked from view during the demonstration, or using spoons they didn't provide themselves, 
            their abilities typically disappear. Laboratory testing of claimed telekinetics has failed to produce any reliable demonstrations of the 
            effect. From a physics perspective, bending metal requires applying force - either mechanical pressure or heat to weaken molecular bonds. 
            The human brain produces electrical activity measured in microvolts, which is many orders of magnitude too weak to exert physical force at 
            a distance. EEG and fMRI studies of individuals attempting telekinesis show no unusual energy emissions or brain activity patterns that 
            could account for such abilities. The most parsimonious explanation for all documented cases of spoon bending is conventional physical 
            manipulation, either overtly or covertly, rather than any paranormal ability.
            """
        },
        {
            'source_id': 'SP003',
            'source': 'Oceanic Research Quarterly',
            'publication_date': '2022-10-08',
            'domain': 'Supernatural Powers',
            'text': """
            The Bermuda Triangle, a loosely defined region in the western part of the North Atlantic Ocean, has become infamous in popular culture 
            for allegedly causing mysterious disappearances of ships and aircraft. However, comprehensive analysis by the United States Coast Guard, 
            insurance companies, and marine researchers has found no evidence that disappearances occur more frequently in this area than in any other 
            heavily trafficked section of ocean. Several factors contribute to the myth: First, the area experiences frequent powerful storms and 
            hurricanes. Second, the Gulf Stream current running through the region can quickly disperse evidence of wrecks. Third, the deep ocean 
            trenches make recovery of wreckage difficult. Fourth, human error is amplified in an oceanic environment where small navigational mistakes 
            can have severe consequences. The mystery was largely created by selective reporting - writers focused on cases with limited information 
            while ignoring the many cases where clear causes were established. Lloyd's of London, the world's leading maritime insurance market, does 
            not recognize the Bermuda Triangle as a special hazard zone and charges no premium for vessels passing through the area. When researchers 
            have traced the history of supposedly "mysterious" disappearances, conventional explanations including weather events, mechanical failure, 
            human error, or piracy have been established for the vast majority of cases.
            """
        },
        {
            'source_id': 'SP003',
            'source': 'Journal of Cultural Anthropology',
            'publication_date': '2023-08-12',
            'domain': 'Supernatural Powers',
            'text': """
            Animal sacrifice, including goat sacrifices, has been practiced in various religious and cultural contexts throughout human history. 
            The sacredness of such practices is entirely dependent on cultural and religious beliefs rather than any empirical evidence of supernatural effects.
            In modern scientific investigation, there is no evidence supporting supernatural claims associated with animal sacrifices. Most contemporary 
            anthropologists and religious scholars view these practices as cultural phenomena that emerged from historical belief systems rather than as 
            objectively "sacred" or possessing supernatural efficacy. In many societies, these practices have been abandoned or transformed for ethical reasons.
            
            From an anthropological perspective, ritual sacrifices often served social functions: reinforcing community bonds, defining religious identity, 
            commemorating significant events, or addressing psychological needs during times of crisis. The perception of sacredness is a cultural attribution 
            rather than an objective quality. The continued practice of animal sacrifice in some cultures is protected as religious expression in many countries,
            but this legal protection acknowledges the subjective cultural importance rather than validating supernatural claims associated with these rituals.
            
            Claims about the supernatural power of animal sacrifices have never been substantiated through controlled studies or empirical evidence. Most reported 
            "effects" can be explained through psychological mechanisms like expectation effects, confirmation bias, and the emotional impact of community rituals.
            """
        }
    ]
    
    # Combine all myths
    all_myths = ghost_myths + ufo_myths + astrology_myths + supernatural_myths
    
    return all_myths
