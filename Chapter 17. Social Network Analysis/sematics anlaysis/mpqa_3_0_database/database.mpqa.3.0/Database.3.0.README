===========================================================

   Documentation for MPQA Opinion Corpus version 3.0

===========================================================

Contents:

  1. Introduction

  2. Overview of Changes

     2.1 Addition of eTarget annotations
     2.2 Addition of targetFrames
     2.3 Revision of target annotations
     2.4 Additional subjectivity annotations

  3. Data

  4. MPQA Annotation Scheme

     4.1 agent
     4.2 expressive-subjectivity
     4.3 direct-subjective
     4.4 objective-speech-event
     4.5 attitude
     4.6 targetFrame
     4.7 sTarget
     4.8 eTarget
     4.9 sentence
     4.10 supplementaryAttitude 
     4.11 supplementaryExpressive-subjectivity

  5. Database Structure

     5.1 database/docs
     5.2 database/meta_anns
     5.3 database/man_anns

  6. GATE Introduction

  7. MPQA Stand-off Annotation Format

  8. Acknowledgements

  9. Contact Information

  10. References

-----------------------------------------------------------

1. Introduction  

This corpus contains news articles and other text documents
manually annotated for opinions and other private states
(i.e., beliefs, emotions, sentiments, speculations, etc.).  

The main changes in this version of the MPQA corpus are the
additions of new eTarget annotations. Previously the target
annotations in MPQA 2.0 are spans. In MPQA 3.0, the eTarget
annotations are entities and events (entity/event-level
target), which are anchored to the heads of noun phrases or
verb phrases. Note that the previous spapn-based target
annotations are retained in this new corpus, which are
renamed as sTarget (span-based target). These changes are
described in more detail in the following section. MPQA 3.0
consists of 70 documents, a subset of previous MPQA. 

-----------------------------------------------------------

2. Overview of Changes

2.1 Addition of eTarget annotations

The MPQA annotation scheme has been extended to include
one new type of annotations: eTarget annotations. The new
annotations are described in (Deng and Wiebe, NAACL 2015).

As an overview, the eTarget annotations aim to specify the
targets of subjectivities to sepcific entities and events.
Previously the targets of subjectivities are span-based. 
A span-based target annotation may contain more than one 
entity or event. The same source may have different
attitudes toward different entities or events in the same
target annotation. Consider the example below.

    When the Imam issued the fatwa
    against Salman Rushdie for insulting
    the Prophet...

By saying ``issued the fatwa against'', Imam has expressed a
negative attitude. Previously the span-based target
annotation of this negative attitude is the whole phrase,
``Salman Rushdie for insulting the Prophet''. In the
sentence, Imam is negative toward Rushdie because he
insulted the  Prophet. Imam is also negative toward the
event of insulting. However, Imam is not negative toward the
Prophet. Actually he is positive toward the Prophet. Thus,
the new eTarget annotations include only ``Rushdie'' and
``insulting'' and do not include ``Prophet''. Then new
developed entity/event-level eTarget annotations in MPQA 3.0
corpus can be used to train a sentiment analysis system
recognizing attitudes toward specific entities and events.

In the current corpus, we recognize the eTargets of
sentiment attitudes and expressive subjectivities. The
eTargets of the other types of attitudes (e.g., arguing,
agreement), and the eTargets of objective speech events are
not added yet. The span-based target annotations in MPQA 2.0
and the eTarget annotations added in MPQA 3.0 are organized
in targetFrames, introduced in the next section.

2.2 Addition of targetFrames

The MPQA corpus has also beed added targetFrames. The
targetFrame annotations are not manually annotated, but are
automatically create to organize the eTarget annotations in
the newly developed corpus and the span-based target
annotations in the previous MPQA corpus in the same
framework.

A targetFrame has beed added to the attitude annotations,
the expressive annotations and the objective speech
annotations. Each targetFrame represents the target of an
attitude, expressive subjectivity or an objective speech
event. The direct subjective annotation does not contain any
targetFrame since it links to attitude annotations. 

A targetFrame contains both span-based target annotations
from MPQA 2.0 corpus, and the entity/event-level eTarget
annotations in the MPQA 3.0 corpus. If there is no such
span-based target or eTarget annotation in a particular
targetFrame, the corresponding entry is ``none''. 

2.3 Revision of target annotations

In the previous MPQA 2.0 corpus, each target annotation is a
span-based word or phrase. Now we introduced the new
entity/event-level eTarget annotations, some of which are
subsumed by the span-based target annotations. A target
annotation is revised to record such subsumming relation. In
short, an eTarget annotation is linked to a target
annotation if the span of target annotation subsumes the
token of the eTarget annotation. Please refer to the section
below for more details. This revision records the
correspondence of eTargets to a span-based target. It would
be useful for previous models which are trained on
span-based target annotations to adapt to this new
entity/event-level eTarget annotations. 

Note that the target annotations are renamed as sTarget
annotations, representing these target are span-based.

2.4 Additional subjectivity annotations

While we are developing the new corpus, we add more
subjectivities, which are only a few. The additional
subjectivites include both attitudes (whose attitude types
are sentiments) and expressive subjectivites. They only
contain eTarget annotations, and do not have target
annotations. 

-----------------------------------------------------------

3. Data

This release of the corpus contains 70 documents, including
the subset of the MPQA original subset that come from
English-language sources (i.e., that are not translations)
and a subset of the OPQA subset.

-----------------------------------------------------------

4. MPQA Annotation Scheme

This section contains an overview of the types of
annotations that you will see marked in the documents of
this corpus. For more details on the MPQA annotations,
please refer to Wilson's thesis
(http://people.cs.pitt.edu/~wiebe/pubs/papers/twilsonDissertation2008.pdf).
For the annotation scheme of this version MPQA 3.0, please
refer to the (Deng and Wiebe, NAACL 2015)
(http://www.aclweb.org/anthology/N/N15/N15-1146.pdf).

Most of the scheme below is the same with previous
annotation scheme. In this version, we distinguish the
required attribute and the optional attribute. Each
annotation of that type have required attributes. The
entries tagged with asterisks are new annotations.

4.1 agent annotation 

    Marks phrases that refer to sources of private states
    and speech events, or phrases that refer to agents who 
    are targets of an attitude.

    Optional attributes:
        id - Unique identifier assigned by the annotator to
             the first meaningful and descriptive reference
             to an agent.

             There are two agent annotations with a 0,0
             byte span in every document.  These two
             annotations are to give an id for the writer
             of the document ('w') and for an implicit
             agent ('implicit').  Private states and
             speech events are sometimes attributed to
             implicit agents.

        nested-source - Used when the agent reference is 
             the source of a private state/speech event. 
             The nested-source is a list of agent ids 
             beginning with the writer and ending with 
             the id for the immediate agent being referenced.

             Example:  w, Foreign Ministry, US State Dept

        agent-uncertain - Used when the annotator is 
             uncertain whether the agent is the correct
             source of a private state/speech event

             Possible values: somewhat-uncertain, very-uncertain

4.2 expressive-subjectivity annotation

    Marks expressive-subjective elements, words and phrases 
    that indirectly express a private state.  For example, 
    'fraud' and 'daylight robbery' in the following sentence 
    are expressive-subjective elements.

    "We foresaw electoral fraud but not daylight robbery,"
    Tsvangirai said.

    Required attributes:
        *id - Identifier assigned to the attitude annotation, 
             typically beginning with an 'ese' followed by a number.

        nested-source - List of agent ids beginning with
             the writer and ending with the id for the 
             immediate agent that is the source of the 
             private state being expressed by the
             expressive-subjective element.

        polarity - Indicates the contextual polarity of the
             private state.

             Possible values: positive, negative, both, neutral,
                uncertain-positive, uncertain-negative, uncertain-both,
                uncertain-neutral

        *targetFrame - Id of a targetFrame that are linked to this
              expressive subjectivity. Each expressive subjectivity
              annoatation has only one targetFrame.

    Optional attributes:
        nested-source-uncertain - Used when an annotator
             is uncertain as to whether the agent is
             the correct nested source.

             Possible values: somewhat-uncertain, very-uncertain

        intensity - Indicates the intensity of private state being
             expressed by the expressive-subjective element.

             Possible values: low, medium, high, extreme

4.3 direct-subjective annotation

    Marks direct mentions of private states and speech
    events (spoken or written) expressing private states.

    Required attributes:
        *id - Identifier assigned to the attitude annotation, 
             typically beginning with an 'ds' followed by a number.

        nested-source - List of agent ids, beginning with
             the writer and ending with the id for the
             immediate agent that is the source of the
             private state or speech event.

        attitude-link - Id of attitude annotation(s) that are linked
             to this direct-subjective annotation.  If there is more
             than one linked attitude, this is represented as a comma-
             separated list of attitude ids.

    Optional attributes:
        annotation-uncertain - Used when an annotator is uncertain
             as to whether the expression marked is indeed
             a direct private state or a speech event.

             Possible values: somewhat-uncertain, very-uncertain

        implicit - The presence of this attribute indicates
             that the speech event is implicit.  This attribute
             is used when there is not a private state or speech
             event phrase on which to actually make an annotation.
             For example, there is no phrase "I write" for the
             writer of the sentence.

        subjective-uncertain - Used when an annotator is
             uncertain as to whether a private state is
             being expressed.

             Possible values: somewhat-uncertain, very-uncertain

        intensity - Indicates the overall intensity of the private 
             state being expressed, considering the 'direct-subjective' 
             phrase and everything inside its scope.

             Possible values: low, medium, high, extreme

        expression-intensity - Indicates the intensity of the 
             speech event or private state expression itself. 
 
             Possible values: neutral, low, medium, high, extreme

        polarity - Indicates the contextual polarity of the
             private state.  Only included when expression-intensity
             is not neutral.

             Possible values: positive, negative, both, neutral,
                uncertain-positive, uncertain-negative, uncertain-both,
                uncertain-neutral

        insubstantial - Used when the private state or
             speech event is not substantial in the discourse

             Possible values are combination of: c1, c2, c3

             These possible values correspond to criteria 
             necessary for a private state or speech event to 
             be substantial.  Please see the annotation
             instructions for a complete description of these
             criteria.  The criteria listed for this attribute
             are the criteria that the private state or speech
             speech event fails to meet.

4.4 objective-speech-event annotation

    Marks speech events that do not express private states.

    Required attributes:
        *id - Identifier assigned to the attitude annotation, 
             typically beginning with an 'ose' followed by a number.

        nested-source - List of agent ids, beginning with
             the writer and ending with the id for the
             immediate agent that is the source of the
             private state or speech event.

        *targetFrame - Id of a targetFrame that are linked to this
              expressive subjectivity. Each objective speech
              event annotation has only one targetFrame.

    Optional attributes:
        annotation-uncertain - Used when an annotator is uncertain
             as to whether the expression marked is indeed
             a speech event.

             Possible values: somewhat-uncertain, very-uncertain

        implicit - The presence of this attribute indicates
             that the speech event is implicit.  This attribute
             is used when there is not a speech event phrase 
             on which to actually make an annotation.
             For example, there is no phrase "I write" for the
             writer of the sentence.

        objective-uncertain - Used when an annotator is
             uncertain as to whether the speech event is objective.

             Possible values: somewhat-uncertain, very-uncertain

        insubstantial - Used when the speech event is not
             substantial in the discourse

             Possible values are combination of: c1, c2, c3

             These possible values correspond to criteria 
             necessary for a private state or speech event to 
             be substantial.  Please see the annotation 
             instructions for a complete description of these 
             criteria.  The criteria listed for this attribute 
             are the criteria that the private state or speech 
             event fails to meet.

4.5 attitude annotation

    Marks the attitudes that compose the expressed private states.

    Required attributes:
        *id - Identifier assigned to the attitude annotation, 
             typically beginning with an 'a' followed by a number.

        attitude-type - Type of attitude

             Possible values:
        		positive sentiment	negative sentiment
        		positive arguing	negative arguing
        		positive agreement	negative agreement (disagreement)
                positive intention	negative intention
        		speculation
        		other-attitude

        *targetFrame - Id of a targetFrame that are linked to this
              expressive subjectivity. Each attitude annotation
              has only one targetFrame.

    Optional attributes:
        attitude-uncertain - Used when an annotator is uncertain
             about the type of attitude, or whether the attitude
             should be marked.

             Possible values: somewhat-uncertain, very-uncertain

        inferred - Used when a fairly prominent attitude can be
             inferred.  For example, in the sentence below, the
             most prominent attitude is a positive sentiment being 
             expressed by the people toward the fall of Chavez.  
             However, there is also clearly a negative attitude
             negative attitude toward Chavez that can be inferred.

             Example: People are happy because Chavez has fallen.

4.6 *targetFrame
    
    Records the span-based target annotations and entity/event-level
    annotations for each attitude, expressive subjectivity and 
    objective speech event. Automatically generated. 

    Required attributes:
        id - Identifier assigned to the attitude annotation, 
             typically beginning with an 'tf' followed by the id
             of the attitude, expressive subjectivity or objective
             speech event annotation that this targetFrame links to.

        sTarget-link - Id of sTarget annotation(s) that are linked
             to this targetFrame.  If there is more
             than one linked sTarget, this is represented as a comma-
             separated list of sTarget ids. If there is no sTarget
             annotated or no sTarget added yet, the entry is ``none''.

        newETarget-link - Id of eTarget annotation(s) that are linked
             to this targetFrame.  The eTarget(s) in this entry are not
             coverer by any span-based target annotation (sTarget). 
             In Figure 1 in (Deng and Wiebe, NAACL 2015), the eTarget(s) 
             are the green eTarget(s). If there is more than one linked 
             eTarget, this is represented as a comma-separated list of 
             sTarget ids. If there is no eTarget outside the sTargets, 
             the entry is ``none''.

4.7 sTarget annotation

    Marks the span-based targets of the attitudes, i.e., 
    what the attitudes are about or what the attitudes 
    are directed toward. Previously the annotations are 
    named as ``target''.

    Required attributes:
        id - Identifier assigned to the target annotation, 
             typically beginning with an 't' followed by a number.

        target-uncertain - Used when an annotator is uncertain
             about whether this is the correct target for the
             attitude.

             Possible values: somewhat-uncertain, very-uncertain

        *eTarget-link - Id of eTarget annotation(s) that are linked
             to this sTarget.  The eTarget(s) in this entry are
             coverer by this sTarget span. If there is more than one 
             linked eTarget, this is represented as a comma-separated 
             list of sTarget ids. If there is no eTarget in this 
             sTarget span or no eTarget added yet, the entry is ``none''.

4.8 *eTarget annotation
    
    Marks the entity/event-level target of the attitudes, 
    expressive subjectivites and objective speech events. 
    The eTarget is anchored to a noun phrase head or a verb 
    phrase head. This annotation is added in the MPQA 3.0 version.

    Required attributes:
        id - Identifier assigned to the target annotation, 
             typically beginning with an 't' followed by a number.

        type - Type of an eTarget

             Possible values:
                entity event other

        isNegated - Whether the entity/event this eTarget 
             refers to represents the negated entity/event. 
             For example, 

                 It is great that the bill was not defeated.

             The eTarget of the positive sentiment ``great'' is 
             ``not defeated''. The token of this eTarget annotation 
             is the word ``defeated''. In this case, the isNegated 
             attribute is yes.
             
             Possible values:
                yes no

    Optional attributes:
        isReferredInSpan - Whether the opinion expression itself
             refers to this eTarget. For example,

                 This idiot breaks the vase.

             The eTarget of the negative expressive subjectivity
             ``This idiot'' is ``idiot'', which is referred in 
             the expressive subjectivity span.

             Possible values:
                yes no

4.9 sentence annotation

    Marks each sentence. This annotation refers to the 
    ``inside'' annotation in the previous MPQA.
    We simply this annotation.

4.10 *supplementaryAttitude annotation

    Marks the attitudes that compose the expressed private 
    states, that we idenfity when developing MPQA 3.0 
    version. The attributes have the same structure with 
    attitude annotations.

4.11 *supplementaryExpressive-subjectivity annotation
    
    Marks expressive-subjective elements, words and phrases 
    that indirectly express a private state, that we identify
    when developing MPQA 3.0 corpus. The attributes 
    have the same structure with expressive-subjectivity
    annotations.

-----------------------------------------------------------

5. Database Structure

The database/ contains three subdirectories: docs,
meta_anns, man_anns. Each subdirectory has the following
structure:
	
		        subdir
		       /      \
		  parent  ..  parent
		 /     \          
	  docleaf  ...  docleaf

Within each subdirectory, each document is uniquely
identified by its parent/docleaf.  For example,
20010927/23.18.15-25073, identifies one document. 20010927
is the parent; 23.18.15-25073 is the docleaf.

5.1 database/docs

    The docs subdirectory contains the document collection.  
    In this subdirectory, each docleaf (e.g., 23.18.15-25073) 
    is a text file containing one document.

5.2 database/meta_anns

    Each docleaf (e.g., 23.18.15-25073) in the meta_anns 
    subdirectory contains information about the document 
    (e.g., source, date).  The meta_anns files are in MPQA 
    format, which is described in Section 6. All the documents
    in the MPQA original subset have corresponding meta_anns 
    files except the following five documents: 20020516/22.23.24-9583, 
    20020517/22.08.22-24562, 20020521/22.21.24-5526, 
    20020522/22.34.49-13286, and 20020523/22.37.46-10374.

5.4 database/gate_anns
    
    This subdirectory contains the annotated files in GATE.
    In this subdirectory, each docleaf is a directory that
    contains one file: gateman.mpqa.3.0.xml.

    The file gateman.mpqa.3.0.xml has the format of a GATE
    annotated file. It can be opened by GATE. The information
    of GATE is introduced in Section 8. It shows the spans of
    annotations and attributes of annotations in the document.
    GATE provides Java API to read and edit the annotations 
    directly.
    
5.3 database/man_anns

    This subdirectory contains the manual annotations for 
    the documents.  In this subdirectory, each docleaf 
    (23.18.15-25073) is a directory that contains two or 
    three files: gateman.mpqa.lre.3.0, gatesentences.mpqa.2.0.

    The file gateman.mpqa.lre.3.0 contains the annotations
    in the MPQA 3.0 corpus. The annotations in gateman.mpqa.lre.3.0
    are the same with annotations in gateman.mpqa.3.0.xml.

    The file gatesentences.mpqa.2.0 contains spans for 
    sentence, minus junk sentences that contain meta data 
    or other spurious information that was not part of the 
    article.  These junk sentences were removed by hand.

    The files, gateman.mpqa.lre.30 and gatesentences.mpqa.2.0
    are in MPQA stand-off format, described in Section 7.

-----------------------------------------------------------

6. GATE Introduction

GATE is a software developed for text annotation and text
processing. We used GATE to annotate the MPQA 3.0 corpus.
The annotated xml files can be loaded directly into GATE and
the users can see the annotations. Note that the annotations
are in the annotation set ``MPQA''. For more details, please
refer to the official website (https://gate.ac.uk/), or a
brief description on the MPQA website
(http://mpqa.cs.pitt.edu/annotation/set_up_gate/). GATE
provides API in Java to read and edit the annotations in xml
files (http://jenkins.gate.ac.uk/job/GATE-Nightly/javadoc/).

-----------------------------------------------------------

7. MPQA Stand-off Format

The MPQA stand-off format is a type of general stand-off
annotation. Every line in an annotation file is either a
comment line (beginning with a '#") or an annotation line
(one annotation per line).  

An MPQA annotation line consists of text fields separated by
a single TAB. The fields used are listed below, with an
example annotation underneath.

id span	    anno_type attributes
58 730,740  agent     nested-source="w,chinarep"

Every annotation has a identifier, id.  This id is unique
ONLY within a given MPQA annotation file. 

The span is the starting and ending byte of the annotation
in the document.  For example, the annotation listed above
is from the document, temp_fbis/20.20.10-3414.  The span of
this annotation is 730,740.  This means that the start of
this annotation is byte 730 in the file
docs/temp_fbis/20.20.10-3414, and byte 740 is the character
after the last character of the annotation.

     blah, blah, blah, example annotation, blah, blah, blah
                       |                 |
                  start byte          end byte

The types of annotations in the gateman.mpqa.lre files
correspond to the annotation types described in Section 4.  

Sentence annotations in the gatesentence.mpqa.2.0 files have
type GATE_sentence.

Each attribute is an attribute_name="attribute_value" pair.
An annotation may have any number of attributes, including 0
attributes.  Multiple attributes for an annotation are
separated by single spaces, and they may be listed in any
order.  The attributes that an annotation may have depends
on the type of annotation.  The set of possible attributes
for each MPQA annotation type is listed in Section 4.

-----------------------------------------------------------

8. Acknowledgements

The development of the MPQA Opinion Corpus version 1.0 
was performed in support of the Northeast Regional Research 
Center (NRRC) which is sponsored by the Advanced Research 
and Development Activity (ARDA), a U.S. Government entity 
which sponsors and promotes research of import to the 
Intelligence Community which includes but is not limited 
to the CIA, DIA, NSA, NIMA, and NRO.

The development of version 1.2 was supported in part by the 
NSF under grant IIS-0208798 and by the Advanced Research 
and Development Activity (ARDA).

The development of version 2.0 was supported in part by an
Andrew Mellow Pre-doctoral Fellowship, Department of
Homeland Security Grant N0014-07-1-0152, and National
Science Foundation grant CNS-0551615. 

The development of version 3.0 was supported in part by an
Andrew Mellow Pre-doctoral Fellowship and DARPA-BAA-12-47
DEFT grant #12475008.

-----------------------------------------------------------

9. Contact Information

Please direct any questions that you have about this corpus or
the annotation scheme to Janyce Wiebe at the University of
Pittsburgh.

Lingjia Deng    email: lid29@pitt.edu
Janyce Wiebe 	email: wiebe@cs.pitt.edu

-----------------------------------------------------------

10. References

Lingjia Deng and Janyce Wiebe (2015). MPQA 3.0:
  Entity/Event-Level Sentiment Corpus. Conference of the North
  American Chapter of the Association for Computational
  Linguistics – Human Language Technologies , Denver,
  Colorado, USA. (NAACL-HLT, 2015.)

Janyce Wiebe, Eric Breck, Chris Buckley, Claire Cardie, 
  Paul Davis, Bruce Fraser, Diane Litman, David Pierce, 
  Ellen Riloff, Theresa Wilson, David Day, Mark Maybury 
  (2003). Recognizing and Organizing Opinions Expressed in 
  the World Press. 2003 AAAI Spring Symposium on New 
  Directions in Question Answering.

Theresa Wilson and Janyce Wiebe (2003). Annotating Opinions 
  in the World Press. 4th SIGdial Workshop on Discourse and 
  Dialogue (SIG0dial-03). ACL SIGdial.

Ellen Riloff, Janyce Wiebe, and Theresa Wilson (2003). 
  Learning Subjective Nouns Using Extraction Pattern 
  Bootstrapping. Seventh Conference on Natural Language
  Learning (CoNLL-03). ACL SIGNLL.

Ellen Riloff and Janyce Wiebe (2003). Learning Extraction
  Patterns for Subjective Expressions. Conference on 
  Empirical Methods in Natural Language Processing (EMNLP-03).
  ACL SIGDAT.

Veselin Stoyanov, Claire Cardie, and Janyce Wiebe (2005). 
Multi-Perspective Question Answering Using the OpQA Corpus.
  Human Language Technologies Conference/Conference on
  Empirical Methods in Natural Language Processing.

Janyce Wiebe, Theresa Wilson, and Claire Cardie (2005).
  Annotating expressions of opinions and emotions in language. 
  Language Resources and Evaluation (formerly Computers and 
  the Humanities) 1(2).

Theresa Wilson, Janyce Wiebe, and Paul Hoffman (2005).
  Recognizing Contextual Polarity in Phrase-Level Sentiment 
  Analysis. Proceedings of HLT/EMNLP 2005, Vancouver, Canada.

Theresa Wilson (2008). Fine-grained Subjectivity and Sentiment
  Analysis: Recognizing the intensity, polarity, and attitudes
  of private states, Chapter 7, "Representing Attitudes and
  Targets".  Ph.D. Dissertation, University of Pittsburgh.

-----------------------------------------------------------

Lingjia Deng
Janyce Wiebe
Yuhuan Jiang

version 3.0  
last modified December 13, 2015
