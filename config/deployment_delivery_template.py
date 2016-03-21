from jinja2 import Environment
import jinja2

manifest_template = """<?xml version="1.0" encoding="UTF-8"?>
<CameraTrapDeployment>
     <ProjectId>{{ deployment['project_id']  | default_none }}</ProjectId>
     <ProjectName>{{ deployment['project_name'] | default_none }}</ProjectName>
     <ProjectObjectives></ProjectObjectives>
     <PublishDate></PublishDate>
    <ProjectOwners>
        <ProjectOwner>{{ deployment['project_owner'] | default_none }}</ProjectOwner>
        <ProjectOwnerEmail>{{ deployment['project_owner_email'] | default_none }}</ProjectOwnerEmail>
    </ProjectOwners>
    <PrincipalInvestigators>
        <PrincipalInvestigator></PrincipalInvestigator>
        <PrincipalInvestigatorEmail></PrincipalInvestigatorEmail>
    </PrincipalInvestigators>
    <ProjectContacts>
        <ProjectContact>{{ deployment['project_contact'] | default_none }}</ProjectContact>
        <ProjectContactEmail></ProjectContactEmail>
    </ProjectContacts>
    <ProjectLatitude></ProjectLatitude>
    <ProjectLongitude></ProjectLongitude>
    <CountryCode>{{ deployment['country_code'] | default_none }}</CountryCode>
    <ProjectDataAccessandUseConstraints></ProjectDataAccessandUseConstraints>
     <SubProjectId>{{ deployment['sub_project_id']  | default_none }}</SubProjectId>
     <SubProjectName>{{ deployment['sub_project_name']  | default_none }}</SubProjectName>
     <SubProjectDesign>{{ deployment['sub_project_design']  | default_none }}</SubProjectDesign>
     <PlotName>{{ deployment['plot_name']  | default_none }}</PlotName>
     <PlotTreatment>{{ deployment['plot_treatment']  | default_none }}</PlotTreatment>
     <CameraDeploymentID>{{ deployment['deployment_id']  | default_none }}</CameraDeploymentID>
     <CameraSiteName>{{ deployment['title']  | default_none }}</CameraSiteName>
     <Originators>
        <OriginatorName>{{ deployment['user_id']  | default_none }}</OriginatorName>
     </Originators>
     <ProposedCameraDeploymentBeginDate>{{ deployment['proposed_date_out']  | default_none }}</ProposedCameraDeploymentBeginDate>
     <ProposedCameraDeploymentEndDate>{{ deployment['proposed_retrieval_date']  | default_none }}</ProposedCameraDeploymentEndDate>
     <ProposedLatitude>{{ deployment['proposed_lat']  | default_none }}</ProposedLatitude>
     <ProposedLongitude>{{ deployment['proposed_long']  | default_none }}</ProposedLongitude>
     <CameraDeploymentBeginDate>{{ deployment['actual_date_out']  | default_none }}</CameraDeploymentBeginDate>
     <CameraDeploymentEndDate>{{ deployment['retrieval_date']  | default_none }}</CameraDeploymentEndDate>
     <CameraDeploymentNotes><![CDATA[ {{ deployment['comments']  | default_none }} ]]></CameraDeploymentNotes>
     <ActualLatitude>{{ deployment['actual_lat']  | default_none }}</ActualLatitude>
     <ActualLongitude>{{ deployment['actual_long']  | default_none }}</ActualLongitude>
     <CameraFailureDetails>{{ deployment['camera_working'] and 'Functioning' or 'Other Failure'  }}</CameraFailureDetails>
     <Bait>No Bait</Bait>
     <BaitDescription></BaitDescription>
     <Feature>{{ deployment['feature']  | default_none }}</Feature>
     <FeatureMethodology></FeatureMethodology>
     <AccessConstraints></AccessConstraints>
     <CameraID>{{ deployment['camera_id']  | default_none }}</CameraID>
     <DetectionDistance>{{ deployment['detection_distance']  | default_none }}</DetectionDistance>
     <QuietPeriodSetting>{{ deployment['quiet_period_setting']  | default_none }}</QuietPeriodSetting>
     <ImageResolutionSetting>{{ deployment['image_resolution_setting']  | default_none }}</ImageResolutionSetting>
     <SensitivitySetting>{{ deployment['sensitivity_setting']  | default_none }}</SensitivitySetting>
     {% for sequence in deployment['sequences'] %}
     <ImageSequence>
        <ImageSequenceId>{{ sequence['sequence_id']  | default_none }}</ImageSequenceId>
        <ImageSequenceBeginTime>{{ sequence['begin_date_time']  | default_none }}</ImageSequenceBeginTime>
        <ImageSequenceEndTime>{{ sequence['end_date_time']  | default_none }}</ImageSequenceEndTime>
           <VolunteerIdentifications>
                {% for ident in sequence['volunteer_identifications'] %}
                <Identification>
                     <IUCNId>{{ ident['species_id']  | default_none }}</IUCNId>
                     <TSNId></TSNId>
                     <SpeciesScientificName>{{ ident['sn']  | default_none }}</SpeciesScientificName>
                     <SpeciesCommonName>{{ ident['cn']  | default_none }}</SpeciesCommonName>
                     <Count>{{ ident['count']  | default_none }}</Count>
                     <Age></Age>
                     <Sex></Sex>
                     <IndividualId></IndividualId>
                     <AnimalRecognizable></AnimalRecognizable>
                     <IndividualAnimalNotes></IndividualAnimalNotes>
                 </Identification>
                 {% endfor %}
           </VolunteerIdentifications>
           <ResearcherIdentifications>
                {% for ident2 in sequence['researcher_identifications'] %}
                <Identification>
                     <IUCNId>{{ ident2['species_id']  | default_none }}</IUCNId>
                     <TSNId></TSNId>
                     <SpeciesScientificName>{{ ident2['sn']  | default_none }}</SpeciesScientificName>
                     <SpeciesCommonName>{{ ident2['cn']  | default_none }}</SpeciesCommonName>
                     <Count>{{ ident2['count']  | default_none }}</Count>
                     <Age></Age>
                     <Sex></Sex>
                     <IndividualId></IndividualId>
                     <AnimalRecognizable></AnimalRecognizable>
                    <IndividualAnimalNotes></IndividualAnimalNotes>
                 </Identification>
                 {% endfor %}
           </ResearcherIdentifications>
           {% for image in sequence['images'] %}
           <Image>
                <ImageId>{{ image['image_id']  | default_none }}</ImageId>
                <ImageFileName>{{ image['file_name']  | default_none }}</ImageFileName>
                <ImageDateTime>{{ image['date_time_original']  | default_none }}</ImageDateTime>
                <ImageOrder>{{ image['image_order']  | default_none }}</ImageOrder>
                <ImageInterestRanking>{{ image['favorite']  | favorite_domain }}</ImageInterestRanking>
                <digitalOrigin>born digital</digitalOrigin>
                <PhotoTypeIdentifications>
                    <PhotoTypeIdentifiedBy></PhotoTypeIdentifiedBy>
                </PhotoTypeIdentifications>
                <RestrictionsonAccess></RestrictionsonAccess>
                <EmbargoPeriodEndDate></EmbargoPeriodEndDate>
                <ImageUseRestrictions></ImageUseRestrictions>
                <ImageIdentifications>
                    <Identification>
                        <IUCNId></IUCNId>
                        <TSNId></TSNId>
                        <SpeciesScientificName></SpeciesScientificName>
                        <SpeciesCommonName></SpeciesCommonName>
                        <Count></Count>
                        <Age></Age>
                        <Sex></Sex>
                        <IndividualId></IndividualId>
                        <AnimalRecognizable></AnimalRecognizable>
                        <IndividualAnimalNotes></IndividualAnimalNotes>
                    </Identification>
                </ImageIdentifications>
           </Image>
          {% endfor %}
     </ImageSequence>
     {% endfor %}
</CameraTrapDeployment>
"""
