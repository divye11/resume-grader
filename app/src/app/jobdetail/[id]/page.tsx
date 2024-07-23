"use client"
import Link from "next/link"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { Collapsible, CollapsibleTrigger, CollapsibleContent } from "@/components/ui/collapsible"
import { ArrowLeftIcon, ChevronRightIcon } from "@/components/icons"
import useApi from "../../../../hooks/useApi"
import { useEffect } from "react"
import Candidate from "@/components/Candidate";

interface JobDetailProps {
  params: {
    id: string;
  };
}

const JobDetail: React.FC<JobDetailProps> = ({ params }) => {
  const { loading, data, error, makeRequest } = useApi<JobDetail>()
  const { loading: loadingCandidates, data: candidatesList, error: candidateError, makeRequest: makeCandidateRequest } = useApi<CandidatesList>()

  useEffect(() => {
    if (params.id && !loading && !data) {
      const jobConfig = {
        url: `jobs/${params.id}`,
        method: 'GET'
      }
      console.log('calling again')
      makeRequest(jobConfig)
    }

    if (!candidatesList && !loadingCandidates) {
      const candidatesConfig = {
        url: `jobs/${params.id}/candidates`,
        method: 'GET'
      }
      makeCandidateRequest(candidatesConfig)
    }

  }, [params.id, loading, makeRequest, data, loadingCandidates, candidatesList, makeCandidateRequest])

  useEffect(() => {
    console.log('data or error', data, error)
  }, [data, error])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.toString()}</div>
  if (!data) return null

  return (
    <div className="max-w-6xl mx-auto py-8 px-4 md:px-6">
      <div className="flex items-center justify-between mb-6">
        <Link
          href="/"
          className="inline-flex items-center gap-2 font-medium text-muted-foreground hover:text-foreground"
          prefetch={false}
        >
          <ArrowLeftIcon className="w-4 h-4" />
          Back
        </Link>
      </div>
      <div className="grid grid-cols-[260px_1fr] gap-8">
        <div className="bg-background border-r p-6">
          <div className="grid gap-4">
            <div className="grid gap-1">
              <div className="text-sm font-medium text-muted-foreground">Job Code</div>
              <div>{data.code || data.shortcode}</div>
            </div>
            <div className="grid gap-1">
              <div className="text-sm font-medium text-muted-foreground">Location</div>
              <div>{data.location?.location_str || 'Not specified'}</div>
            </div>
          </div>
        </div>
        <div className="grid gap-8">
          <div className="grid gap-4">
            <h1 className="text-3xl font-bold">{data.full_title}</h1>
            <div className="grid sm:grid-cols-2 gap-4">
              <div className="grid gap-1">
                <div className="text-sm font-medium text-muted-foreground">Department</div>
                <div>{data.department || 'Not specified'}</div>
              </div>
              <div className="grid gap-1">
                <div className="text-sm font-medium text-muted-foreground">Employment Type</div>
                <div>{data.employment_type || 'Not specified'}</div>
              </div>
            </div>
          </div>
          <div className="grid gap-6">
            <div className="grid gap-2">
              <h2 className="text-xl font-semibold">Job Description</h2>
              <div className="text-muted-foreground" dangerouslySetInnerHTML={{ __html: data.description }} />
            </div>
            <div className="grid gap-2">
              <h2 className="text-xl font-semibold">Requirements</h2>
              <div className="text-muted-foreground" dangerouslySetInnerHTML={{ __html: data.requirements }} />
            </div>
            <div className="grid gap-2">
              <h2 className="text-xl font-semibold">Benefits</h2>
              <div className="text-muted-foreground" dangerouslySetInnerHTML={{ __html: data.benefits }} />
            </div>
            <div className="grid gap-2">
              <h2 className="text-xl font-semibold">Industry</h2>
              <div className="text-muted-foreground">{data.industry}</div>
            </div>
          </div>
          <div className="grid gap-6">
            <h2 className="text-xl font-semibold">Candidates</h2>
            <div className="grid gap-4">
              {loadingCandidates ? (
                <div>Loading candidates...</div>
              ) : candidateError ? (
                <div>Error loading candidates: {candidateError.toString()}</div>
              ) : candidatesList && candidatesList?.candidates?.length > 0 ? (
                candidatesList.candidates.map((candidate) => (
                  <Candidate
                    id={candidate.id}
                    key={candidate.id}
                    name={candidate.name}
                    stage={candidate?.stage || ''}
                    relevancyScore={0.1}
                  />
                ))
              ) : (
                <div>No candidates found for this job.</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobDetail