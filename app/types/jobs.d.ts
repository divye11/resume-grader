interface DepartmentHierarchy {
   id: number;
   name: string;
}

interface Location {
   location_str?: string;
   country?: string;
   country_code?: string;
   region?: string;
   region_code?: string;
   city?: string;
   zip_code?: string;
   telecommuting: boolean;
   workplace_type: string;
}

interface LocationDetail {
   country_code?: string;
   country_name?: string;
   state_code?: string;
   subregion?: string;
   zip_code?: string;
   city?: string;
   coords: string;
   hidden: boolean;
}

interface Job {
   id: string;
   title: string;
   full_title: string;
   shortcode: string;
   code?: string;
   state: string;
   sample: boolean;
   department?: string;
   department_hierarchy: DepartmentHierarchy[];
   url: HttpUrl;
   application_url: HttpUrl;
   shortlink: HttpUrl;
   location?: Location;
   locations?: LocationDetail[];
   created_at: DateTime;
}

interface JobsList {
   jobs: Job[];
}

interface JobDetail {
   id: string;
   title: string;
   full_title: string;
   shortcode: string;
   code?: string;
   state: string;
   department?: string;
   department_hierarchy: DepartmentHierarchy[];
   url: HttpUrl;
   application_url: HttpUrl;
   shortlink: HttpUrl;
   location?: Location;
   locations?: LocationDetail[];
   created_at: DateTime;
   full_description: string;
   description: string;
   requirements: string;
   benefits: string;
   employment_type: string;
   industry: string;
   function?: string;
   experience?: string;
   education?: string;
   keywords?: string;
}
interface Candidate {
   id: string;
   name: string;
   firstname: string;
   lastname: string;
   headline?: string;
   account: Account;
   job: JobInfo;
   stage: string;
   disqualified: boolean;
   disqualification_reason?: string;
   hired_at?: Date;
   sourced: boolean;
   profile_url: HttpUrl;
   address?: string;
   phone?: string;
   email: string;
   domain?: string;
   created_at: Date;
   updated_at: Date;
}

interface CandidatesList {
   candidates: Candidate[];
}
