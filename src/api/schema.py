# municipalities
# 	- id
# 	- name
# 	- type (town/city/county/state)

class Municipality(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey(municipality.id))
    parent: Mapped[Municipality] = relationship(remote_side([id]))
    name: Mapped[str]
    type: Mapped[MunicipalityType]
    

# office_templates
# 	- id
# 	- title
# 	- description

class OfficeTemplate(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    desription: Mapped[MunicipalityType]
    

# offices
# 	- id
# 	- municipality_id (FK)
# 	- title
# 	- description
# 	- elected (Something we want to track, like clerks may not be elected)
# 	- tenure (in months? days?)
# 	- salary
# 	- min_hours
# 	- max_hours

class Office(BaseModel):
	id: Mapped[int] = mapped_column(primary_key=True)
	municipality_id: Mapped[int] = mapped_column(ForeignKey('municipality.id'))
	municipality: Mapped[Municipality] = relationship()
	title: Mapped[str]
	description: Mapped[str]
	elected: Mapped[bool] = mapped_column(server_default=TRUE)
	tenure: Mapped[int]
	salary: Mapped[int]
	min_hours: Mapped[int]
	max_hours: Mapped[int]



# officials
# 	- id
# 	- municipality_id (FK)
# 	- office_id (FK)
# 	- term_id (FK)
# 	- name

class Official(BaseModel):
	id: Mapped[int] = mapped_column(primary_key=True)
	municipality_id: Mapped[int] = mapped_column(ForeignKey('municipality.id'))
	municipality: Mapped[Municipality] = relationship()
	office_id: Mapped[Optional[int]] = mapped_column(ForeignKey('office.id'))
	office: Mapped[Office] = relationship()
	term_id: Mapped[int] = mapped_column(ForeignKey('term.id'))
	term: Mapped[Term] = relationship()
	name: Mapped[str]
	phone: Mapped[str]
	email: Mapped[str]
	contact_form: Mapped[str]

	
# candidates
# 	- id 
# 	- municipality_id (FK)
# 	- election_id (FK)

class Candidate(BaseModel):
	id: Mapped[int] = mapped_column(primary_key=True)
	municipality_id: Mapped[int] = mapped_column(ForeignKey('municipality.id'))
	municipality: Mapped[Municipality] = relationship()
	election_id: Mapped[int] = mapped_column(ForeignKey(election.id))
	election: Mapped[Election] = relationship()


# terms
# 	- id,
# 	- start,
# 	- end,
# 	- incumbents: [],

class Term(BaseModel):
	id: Mapped[int] = mapped_column(primary_key=True)
	election_id: Mapped[int] mapped_column(ForeignKey('election.id'))
	election: Mapped[Election] = relationship()
	start: Mapped[datetime.date]
	end: Mapped[datetime.date]
	incumbents: Mapped[List[Official]] = relationship()


# elections
# 	- id
# 	- municipality_id (FK)
# 	- office_id (FK)
# 	- term_id (FK)
# 	- type (primary/general/special)
# 	- election_date

class ElectionType(str, Enum):
    PRIMARY = "primary"
    GENERAL = "general"
    SPECIAL = "special"

class Election(BaseModel):
	id: Mapped[int] = mapped_column(primary_key=True)
	municipality_id: Mapped[int] = mapped_column(ForeignKey('municipality.id'))
	municipality: Mapped[Municipality] = relationship()
	office_id: Mapped[Optional[int]] = mapped_column(ForeignKey('office.id'))
	office: Mapped[Office] = relationship()
	term_id: Mapped[int] = mapped_column(ForeignKey('term.id'))
	term: Mapped[Term] = relationship()
	type: Mapped[ElectionType]
	election_date: Mapped[datetime.date]
	

	
# requirements
# 	- id 
# 	- form_id (FK)
# 	- deadline_id (FK)
# 	- title
# 	- description
# 	- deadline

# forms 
# 	- id
# 	- title
# 	- description
# 	- url

# deadlines
# 	- id 
# 	- municipality_id (FK)
# 	- title
# 	- description
# 	- deadline

