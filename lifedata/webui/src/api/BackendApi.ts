import { SampleViewConfig } from "../SampleViewConfig";
import { Label } from "../labels";
import { Sample } from "../Sample";
import { User } from "../User";
import { IApi } from "./index";
import { LabelConfig } from "../labels";
import { StringConfig } from "../ui_strings";
import { AnnotationQueueConfig, QueuedSamples } from "../queues";
import { AnnotationCountDefinition } from "../counts";

type Options = {
  url: string;
};

type RequestOptions = {
  token?: string;
};

function getApiUrl() {
  if (process.env.REACT_APP_API_URL === undefined) {
    throw new Error("REACT_APP_API_URL not defined");
  }

  return process.env.REACT_APP_API_URL;
}

export default class BackendApi implements IApi {
  token: string | null = null;
  options: Options = {
    url: getApiUrl(),
  };

  constructor(options: Partial<Options> = {}) {
    this.options = Object.assign({}, this.options, options);
  }

  _getRequestOptions(options: RequestOptions) {
    const token = options.token !== undefined ? options.token : this.token;
    const headers = {
      "Content-Type": "application/json",
      ...(token !== null
        ? {
            "X-Auth-Token": token,
          }
        : {}),
    };
    return { headers };
  }

  _get(path: string, options: RequestOptions = {}) {
    return fetch(
      `${this.options.url}${path}`,
      this._getRequestOptions(options)
    );
  }

  _post(
    path: string,
    body: object | null = null,
    options: RequestOptions = {}
  ) {
    return fetch(`${this.options.url}${path}`, {
      method: "POST",
      body: body === null ? "" : JSON.stringify(body),
      ...this._getRequestOptions(options),
    });
  }

  async authenticate(token: string): Promise<User> {
    return this._get(`/auth/`, { token }).then((response) => {
      if (response.status !== 200) {
        return Promise.reject();
      }
      this.token = token;
      return response.json() as Promise<User>;
    });
  }

  async logout() {
    this.token = null;
    return Promise.resolve(undefined);
  }

  async getSampleByID(sampleId: String) {
    return this._get(`/samples/by-id/${sampleId}/`).then((response) => {
      // NOTE: This may not be the matching response codes but in this short time the best I could realize
      if (response.status === 418) {
        return Promise.resolve({ status: "no-samples-left", sample: null });
      } else if (response.status === 204) {
        return Promise.resolve({ status: "no-initial-samples", sample: null });
      } else if (response.status === 429) {
        return Promise.resolve({
          status: "waiting-for-training-to-finish",
          sample: null,
        });
      } else if (response.status === 404) {
        return Promise.resolve({ status: "sample-not-found", sample: null });
      } else {
        return response
          .json()
          .then((sample) => ({ status: "ok", sample: sample }));
      }
    }) as Promise<
      | { status: "no-initial-samples"; sample: null }
      | { status: "no-samples-left"; sample: null }
      | { status: "waiting-for-training-to-finish"; sample: null }
      | { status: "sample-not-found"; sample: null }
      | { status: "ok"; sample: Sample }
    >;
  }

  async getCurrentSample() {
    return this._get(`/samples/next/`).then((response) => {
      // NOTE: This may not be the matching response codes but in this short time the best I could realize
      if (response.status === 418) {
        return Promise.resolve({ status: "no-samples-left", sample: null });
      } else if (response.status === 204) {
        return Promise.resolve({ status: "no-initial-samples", sample: null });
      } else if (response.status === 429) {
        return Promise.resolve({
          status: "waiting-for-training-to-finish",
          sample: null,
        });
      } else if (response.status === 404) {
        return Promise.resolve({ status: "sample-not-found", sample: null });
      } else {
        return response
          .json()
          .then((sample) => ({ status: "ok", sample: sample }));
      }
    }) as Promise<
      | { status: "no-initial-samples"; sample: null }
      | { status: "no-samples-left"; sample: null }
      | { status: "waiting-for-training-to-finish"; sample: null }
      | { status: "sample-not-found"; sample: null }
      | { status: "ok"; sample: Sample }
    >;
  }

  async getAnnotationCount() {
    return this._get(`/count-by-annotator/`).then(
      (response) => response.json() as Promise<AnnotationCountDefinition>
    );
  }

  async submitSample(sample: Sample, labels: Label[]) {
    const body = {
      labels,
    };
    return this._post(
      `/samples/annotate/${encodeURIComponent(sample.id)}/`,
      body
    ).then((response) => {
      if (response.status !== 200 && response.status !== 201) {
        return Promise.reject();
      }
      return undefined;
    });
  }

  async consultColleague(sample: Sample, queue_name: string, labels: Label[]) {
    const body = {
      labels,
      queue_name,
    };
    return this._post(
      `/samples/consult/${encodeURIComponent(sample.id)}/`,
      body
    ).then((response) => {
      if (response.status !== 200 && response.status !== 201) {
        return Promise.reject();
      }
      return undefined;
    });
  }

  async skipSample(sample: Sample) {
    return this._post(`/samples/skip/${encodeURIComponent(sample.id)}/`).then(
      (response) => {
        if (response.status !== 200 && response.status !== 201) {
          return Promise.reject();
        }
        return undefined;
      }
    );
  }

  async getUiStrings() {
    return this._get(`/sampleview/strings/`).then(
      (response) => response.json() as Promise<StringConfig>
    );
  }

  async getSampleViewConfig() {
    return this._get(`/sampleview/config/`).then(
      (response) => response.json() as Promise<SampleViewConfig>
    );
  }

  async getLabels() {
    return this._get(`/labels/`).then(
      (response) => response.json() as Promise<LabelConfig>
    );
  }

  async getAnnotationQueueConfig() {
    return this._get(`/annotationqueueconfig/`).then(
      (response) => response.json() as Promise<AnnotationQueueConfig>
    );
  }

  async getQueuedSamples() {
    return this._get(`/queuedsamples/`).then(
      (response) => response.json() as Promise<QueuedSamples>
    );
  }
}
